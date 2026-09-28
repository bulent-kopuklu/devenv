#!/usr/bin/env python3
"""`devenv create` senaryolari, nix build'siz: devenv modul olarak yuklenir,
build ve speckit yakalanir. Her kosu gecici dizinlerde; global config'e ve
repoya bir sey yazmaz.

    python3 -B tests/devenv_create.py
"""
import importlib.machinery, importlib.util, io, json, os, re, shutil, subprocess, sys, tempfile
from contextlib import redirect_stdout
from pathlib import Path

sys.dont_write_bytecode = True  # bin/__pycache__ kalirsa install.sh onu tool sanar
DEVENV = Path(__file__).resolve().parents[1] / "bin" / "devenv"
WORK = Path(tempfile.mkdtemp(prefix="devenv-test-"))
CFG = WORK / "cfg"
os.environ["CLAUDE_CONFIG_DIR"] = str(CFG)
CFG.mkdir(); (CFG / "CLAUDE.md").write_text("# global kurallar\n")
results = []


def load():
    loader = importlib.machinery.SourceFileLoader("devenv", str(DEVENV))
    m = importlib.util.module_from_spec(importlib.util.spec_from_loader("devenv", loader))
    loader.exec_module(m)
    m.build = lambda: print("[build atlandi]")
    m.speckit = lambda: print("[speckit]")
    return m


def devenv(cwd, *argv, answer=""):
    """`answer`, dolu dizinde sorulan ezme sorusunun cevabi; soru ciktiya duser."""
    os.chdir(cwd)
    m = load()
    m.input = lambda prompt: print(prompt) or answer
    sys.argv = ["devenv", *argv]
    out, code = io.StringIO(), 0
    with redirect_stdout(out):
        try:
            m.main()
        except SystemExit as e:
            code = e.code
    return out.getvalue(), code


def ok(code):
    return code in (0, None)


def check(name, cond):
    print(("OK   " if cond else "FAIL ") + name)
    results.append(bool(cond))


def settings(p):
    try:
        return json.loads(Path(p).read_text())["permissions"]
    except (OSError, ValueError, KeyError) as e:
        print(f"     {p}: {e}")
        return {"deny": [], "allow": [], "additionalDirectories": []}


def speckit_template(rel, name):
    return (DEVENV.parents[1] / "templates/speckit/project" / rel).read_text().replace("{{NAME}}", name)


def git_init(path):
    subprocess.run(["git", "init", "-q", str(path)], check=True)


# yeni proje
t = WORK / "yeni"; t.mkdir()
out, code = devenv(t, "create", "ornek", "--lang", "go", "--speckit")
root, impl, ctrl = t / "ornek", t / "ornek/ornek-impl", t / "ornek/ornek-ctrl"
check("yeni: cikis 0", ok(code))
check("yeni: bos dizinde soru yok", "ezeyim mi" not in out)
check("yeni: ust dizin repo degil", not (root / ".git").exists())
check("yeni: impl repo, ctrl degil", (impl / ".git").is_dir() and not (ctrl / ".git").exists())
check("yeni: ust CLAUDE.md protokolu tasir", "## Çalışma sırası" in (root / "CLAUDE.md").read_text())
check("yeni: rol metinleri ve Makefile sozlesmesi .claude/rules altinda",
      (ctrl / ".claude/rules/main-rules.md").is_file() and (impl / ".claude/rules/main-rules.md").is_file()
      and (impl / ".claude/rules/makefile.md").is_file())
check("yeni: proje dosyalari config'ten import etmez",
      not any(f"@{CFG}" in p.read_text() for p in root.rglob("*.md") if ".git" not in p.parts))
check("yeni: ctrl CLAUDE.md", (ctrl / "CLAUDE.md").is_file())
check("yeni: ctrl feature-branch.sh impl yolunu tasir", f'impl="{t}/ornek/ornek-impl"' in (ctrl / "scripts/feature-branch.sh").read_text() and os.access(ctrl / "scripts/feature-branch.sh", os.X_OK))
check("yeni: ctrl reviewer agent'i", (ctrl / ".claude/agents/reviewer.md").is_file())
check("yeni: review global kurallari projedeki kopyadan okur",
      (ctrl / ".claude/skills/review/global-rules.md").read_text() == "# global kurallar\n"
      and f"`{ctrl}/.claude/skills/review/global-rules.md`" in (ctrl / ".claude/skills/review/SKILL.md").read_text())
check("yeni: hicbir proje dosyasi config dizinine gitmez",
      not any(str(CFG) in p.read_text() for p in root.rglob("*") if p.is_file() and ".git" not in p.parts))
check("yeni: ctrl skill'leri", all((ctrl / ".claude/skills" / s / "SKILL.md").is_file()
                                   for s in ("reference", "review")))
check("yeni: impl CLAUDE.md speckit sablonundan, templates/claude'dan degil",
      (impl / "CLAUDE.md").read_text() == speckit_template("impl/CLAUDE.md", "ornek"))
check("yeni: baslik proje adi, dizin adi degil", (root / "CLAUDE.md").read_text().startswith("# ornek\n"))
check("yeni: yer tutucu kalmadi", not any(re.search(r"\{\{[A-Z]+\}\}", p.read_text()) for p in root.rglob("*")
                                         if p.is_file() and ".git" not in p.parts))
check("yeni: Makefile dilsiz iskelet, proje adi argumandan",
      (impl / "Makefile").read_text()
      == (DEVENV.parents[1] / "templates/make/Makefile").read_text().replace("{{NAME}}", "ornek"))
check("yeni: dilin Makefile bilgisi kuralinda", "## Makefile'da Go bileşeni" in (impl / ".claude/rules/go.md").read_text())
check("yeni: speckit cagrildi", "[speckit]" in out)
anayasa = impl / ".specify/memory/constitution.md"
check("yeni: anayasa yazildi, proje adiyla", anayasa.is_file() and anayasa.read_text().startswith("# ornek Anayasası\n"))
check("yeni: oturum komutlari basildi", "claude -n ornek-impl" in out and "claude -n ornek-ctrl" in out)
cs, ls = settings(ctrl / ".claude/settings.json"), settings(impl / ".claude/settings.local.json")
check("yeni: ctrl impl'e yazamaz", f"Edit(/{impl}/**)" in cs["deny"] and cs["deny"][0].startswith("Edit(//"))
check("yeni: ctrl impl'i ve wiki'yi okur", str(impl) in cs["additionalDirectories"] and len(cs["additionalDirectories"]) == 2)
check("yeni: impl ctrl'e yazamaz, ctrl'i okuyamaz",
      f"Edit(/{ctrl}/**)" in ls["deny"] and f"Read(/{ctrl}/**)" in ls["deny"]
      and str(ctrl) not in ls.get("additionalDirectories", []))
check("yeni: iki rolde autocompact esigi %60",
      all(json.loads(p.read_text()).get("env", {}).get("CLAUDE_AUTOCOMPACT_PCT_OVERRIDE") == "61"
          for p in (ctrl / ".claude/settings.json", impl / ".claude/settings.local.json")))
check("yeni: iki rolde compact ozeti Turkce",
      all("Türkçe" in h["command"]
          for p in (ctrl / ".claude/settings.json", impl / ".claude/settings.local.json")
          for m in json.loads(p.read_text())["hooks"]["PreCompact"] for h in m["hooks"]))
check("yeni: impl spike cagiramaz", "Skill(spike)" in ls["deny"] and "Skill(spike *)" in ls["deny"])
check("yeni: impl'in yuklediklerinde ctrl'in yolu yok",
      str(ctrl) not in (impl / "CLAUDE.local.md").read_text())
excl = (impl / ".git/info/exclude").read_text()
check("yeni: yerel dosyalar exclude'da",
      all(f in excl for f in ("CLAUDE.local.md", ".claude/settings.local.json")))
check("yeni: urun dosyalari exclude'da degil",
      not any(f in excl.splitlines() for f in ("CLAUDE.md", ".gitignore", ".envrc", ".golangci.yml", "Makefile")))
check("yeni: impl commit, push ve gate'e izinli",
      all(r in ls["allow"] for r in ("Bash(git add *)", "Bash(git commit *)", "Bash(git push *)", "Bash(make *)")))
check("yeni: ctrl branch script'i ve impl commit'ine izinli",
      "Bash(scripts/feature-branch.sh *)" in cs["allow"] and f"Bash(git -C {impl} commit *)" in cs["allow"])
status = subprocess.run(["git", "-C", str(impl), "status", "--porcelain"], capture_output=True, text=True).stdout
check("yeni: yerel dosyalar git status'ta yok", "CLAUDE.local.md" not in status and "settings.local" not in status)

# dolu dizin: once sorar; N ise dokunmaz, y ise ustune yazar ve silmez
(impl / "CLAUDE.md").write_text("# degisti\n")
(impl / ".specify/memory/constitution.md").write_text("# degisti\n")
(impl / "kendi.txt").write_text("kullanicinin\n")
(impl / ".claude/settings.local.json").write_text(json.dumps({"permissions": {"allow": ["Bash(ls)"]}}))
out, code = devenv(t, "create", "ornek", "-l", "go", "--speckit", answer="n")
check("dolu N: soruldu", "ezeyim mi" in out)
check("dolu N: cikis 0 degil", not ok(code))
check("dolu N: dokunulmadi", (impl / "CLAUDE.md").read_text() == "# degisti\n" and "[speckit]" not in out)
out, code = devenv(t, "create", "ornek", "-l", "go", "--speckit", answer="y")
check("dolu y: soruldu", "ezeyim mi" in out)
check("dolu y: cikis 0", ok(code))
check("dolu y: CLAUDE.md sablonla ezildi", (impl / "CLAUDE.md").read_text() == speckit_template("impl/CLAUDE.md", "ornek"))
check("dolu y: izinler birlesmedi, sablonla ezildi",
      "Bash(ls)" not in settings(impl / ".claude/settings.local.json")["allow"])
check("dolu y: baska dosya silinmedi", (impl / "kendi.txt").read_text() == "kullanicinin\n")
check("dolu y: Spec Kit yeniden kuruldu", "[speckit]" in out)
check("dolu y: anayasa sablonla ezildi", (impl / ".specify/memory/constitution.md").read_text().startswith("# ornek Anayasası\n"))
check("dolu y: exclude tekrarlanmadi", (impl / ".git/info/exclude").read_text().count("CLAUDE.local.md") == 1)

# dil ekleme: go ile baslanan projeye sonradan rust modulu
t = WORK / "ekle"; t.mkdir()
out, code = devenv(t, "create", "ornek", "-l", "go", "--speckit")
impl = t / "ornek/ornek-impl"
with open(impl / "Makefile", "a") as f:
    f.write("\nprojenin-hedefi:\n\t@true\n")
(impl / "rustfmt.toml").write_text("max_width = 80\n")
once = {f: (impl / f).read_text() for f in ("CLAUDE.md", "CLAUDE.local.md", ".golangci.yml", "Makefile",
                                             ".claude/rules/go.md", ".claude/rules/main-rules.md")}
out, code = devenv(impl, "add", "-l", "rust")
check("ekle: cikis 0", ok(code))
check("ekle: flake'te go ve rust", 'langs = [ "go" "rust" ];' in (impl / "flake.nix").read_text())
check("ekle: rust kurallari ve dosyalari geldi", (impl / ".claude/rules/rust.md").is_file() and (impl / "clippy.toml").is_file())
check("ekle: var olan dosya ezilmedi", (impl / "rustfmt.toml").read_text() == "max_width = 80\n")
check("ekle: Makefile, go'nun ve rollerin dosyalari degismedi", all((impl / f).read_text() == v for f, v in once.items()))
check("ekle: Spec Kit'e dokunulmadi", "[speckit]" not in out)
out, code = devenv(impl, "add", "-l", "rust", "-l", "go")
check("ekle: var olan dil yeniden eklenmez",
      ok(code) and "zaten var" in out and 'langs = [ "go" "rust" ];' in (impl / "flake.nix").read_text())
out, code = devenv(t, "add", "-l", "rust")
check("ekle: urun reposu disinda reddedilir", not ok(code))

# --speckit'siz: proje dizini urun reposu
t = WORK / "tek"; t.mkdir()
out, code = devenv(t, "create", "ornek", "--lang", "go")
p = t / "ornek"
check("tek: cikis 0", ok(code))
check("tek: proje dizini repo", (p / ".git").is_dir())
check("tek: impl ve ctrl yok", not (p / "ornek-impl").exists() and not (p / "ornek-ctrl").exists())
check("tek: CLAUDE.md kokte, baslik proje adi", (p / "CLAUDE.md").read_text().startswith("# ornek\n"))
check("tek: Makefile ve dil kurallari kokte", (p / "Makefile").is_file() and (p / ".claude/rules/go.md").is_file())
ignored = lambda f: subprocess.run(["git", "-C", str(p), "check-ignore", "-q", f]).returncode == 0
check("tek: editor ayari .vscode'da ve git'e girer", (p / ".vscode/settings.json").is_file() and not ignored(".vscode/settings.json"))
check("tek: Makefile proje adini tasir", "PROJECT    := ornek\n" in (p / "Makefile").read_text())
check("tek: rol dosyalari yok", not (p / "CLAUDE.local.md").exists() and not (p / ".claude/settings.local.json").exists())
check("tek: Spec Kit yok", "[speckit]" not in out and not (p / ".specify").exists())
check("tek: tek oturum basildi", "claude -n ornek\n" in out and "ornek-impl" not in out)
t = WORK / "tek-repo" / "repo"; t.mkdir(parents=True); git_init(t)
out, code = devenv(t.parent, "create", "repo", "--lang", "go", answer="y")
check("tek repo: var olan repoda kurulur", ok(code) and (t / "CLAUDE.md").read_text().startswith("# repo\n"))

# create . : bulunulan dizin proje dizini; ayni kural
t = WORK / "nokta" / "nokta"; t.mkdir(parents=True)
out, code = devenv(t, "create", ".", "--lang", "go")
check("nokta: cikis 0", ok(code))
check("nokta: bos dizinde soru yok", "ezeyim mi" not in out)
check("nokta: bulunulan dizin repo", (t / ".git").is_dir() and not (t / "nokta-impl").exists())
check("nokta: ic ice dizin yok", not (t / "nokta").exists())
check("nokta: baslik dizinin adi", (t / "CLAUDE.md").read_text().startswith("# nokta\n"))
t = WORK / "nokta-speckit" / "iki"; t.mkdir(parents=True)
out, code = devenv(t, "create", ".", "--lang", "go", "--speckit")
check("nokta speckit: impl ve ctrl bulunulan dizinde", ok(code) and (t / "iki-impl/.git").is_dir() and (t / "iki-ctrl/CLAUDE.md").is_file())
check("nokta speckit: baslik dizinin adi", (t / "CLAUDE.md").read_text().startswith("# iki\n"))
t = WORK / "nokta-dolu" / "dolu"; t.mkdir(parents=True); (t / "notlar.md").write_text("x\n")
out, code = devenv(t, "create", ".", "--lang", "go", answer="n")
check("nokta dolu N: soruldu, dokunulmadi", "ezeyim mi" in out and not ok(code) and not (t / ".git").exists())
out, code = devenv(t, "create", ".", "--lang", "go", answer="y")
check("nokta dolu y: kuruldu, dosya silinmedi", ok(code) and (t / ".git").is_dir() and (t / "notlar.md").is_file())

# reddedilenler
t = WORK / "red"; (t / "repo").mkdir(parents=True); git_init(t / "repo")
out, code = devenv(t, "create", "repo", "--lang", "go", "--speckit")
check("red: speckit'te ust dizin repo ise", not ok(code) and "ust dizin repo olamaz" in str(code))
out, code = devenv(t, "go")
check("red: alt komutsuz cagri", not ok(code))
out, code = devenv(t, "create", "x/y", "--lang", "go")
check("red: adda '/'", not ok(code))
out, code = devenv(t, "create", "ornek", "go")
check("red: dil -l'siz", not ok(code))

if all(results):
    shutil.rmtree(WORK)
    print(f"\n{len(results)}/{len(results)} gecti")
else:
    print(f"\n{sum(results)}/{len(results)} gecti; incelemek icin: {WORK}")
sys.exit(0 if all(results) else 1)
