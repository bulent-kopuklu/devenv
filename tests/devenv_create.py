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
check("yeni: ust CLAUDE.md protokolu import eder", f"@{CFG}/roles/protocol.md" in (root / "CLAUDE.md").read_text())
check("yeni: ctrl CLAUDE.md rolu import eder", f"@{CFG}/roles/ctrl.md" in (ctrl / "CLAUDE.md").read_text())
check("yeni: ctrl CLAUDE.md", (ctrl / "CLAUDE.md").is_file())
check("yeni: ctrl feature-branch.sh impl yolunu tasir", f'impl="{t}/ornek/ornek-impl"' in (ctrl / "scripts/feature-branch.sh").read_text() and os.access(ctrl / "scripts/feature-branch.sh", os.X_OK))
check("yeni: ctrl reviewer agent'i", (ctrl / ".claude/agents/reviewer.md").is_file())
check("yeni: review global CLAUDE.md'yi mutlak yolla okur",
      f"`{CFG}/CLAUDE.md`" in (ctrl / ".claude/skills/review/SKILL.md").read_text()
      and f"Read(/{CFG}/CLAUDE.md)" in settings(ctrl / ".claude/settings.json")["allow"])
check("yeni: ctrl skill'leri", all((ctrl / ".claude/skills" / s / "SKILL.md").is_file()
                                   for s in ("reference", "review")))
check("yeni: impl CLAUDE.local.md rolu import eder", f"@{CFG}/roles/impl.md" in (impl / "CLAUDE.local.md").read_text())
check("yeni: baslik proje adi, dizin adi degil", (impl / "CLAUDE.md").read_text().startswith("# ornek\n"))
check("yeni: yer tutucu kalmadi", not any(re.search(r"\{\{[A-Z]+\}\}", p.read_text()) for p in root.rglob("*")
                                         if p.is_file() and ".git" not in p.parts))
mk = (impl / "Makefile").read_text()
check("yeni: Makefile yalniz go ve proto parcasi", "go_build" in mk and "proto_lint" in mk and "cargo" not in mk and "cmake" not in mk and "npm" not in mk)
check("yeni: Makefile gate hedefi", "\ngate:" in mk and "\ntest-integration:" in mk)
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
      all(r in ls["allow"] for r in ("Bash(git add *)", "Bash(git commit *)", "Bash(git push *)", "Bash(make gate)")))
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
check("dolu y: CLAUDE.md sablonla ezildi", (impl / "CLAUDE.md").read_text().startswith("# ornek\n"))
check("dolu y: izinler birlesmedi, sablonla ezildi",
      "Bash(ls)" not in settings(impl / ".claude/settings.local.json")["allow"])
check("dolu y: baska dosya silinmedi", (impl / "kendi.txt").read_text() == "kullanicinin\n")
check("dolu y: Spec Kit yeniden kuruldu", "[speckit]" in out)
check("dolu y: anayasa sablonla ezildi", (impl / ".specify/memory/constitution.md").read_text().startswith("# ornek Anayasası\n"))
check("dolu y: exclude tekrarlanmadi", (impl / ".git/info/exclude").read_text().count("CLAUDE.local.md") == 1)

# create . : bulunulan dizin proje dizini; ayni kural
t = WORK / "nokta" / "nokta"; t.mkdir(parents=True)
out, code = devenv(t, "create", ".", "--lang", "go")
check("nokta: cikis 0", ok(code))
check("nokta: bos dizinde soru yok", "ezeyim mi" not in out)
check("nokta: impl ve ctrl bulunulan dizinde", (t / "nokta-impl/.git").is_dir() and (t / "nokta-ctrl/CLAUDE.md").is_file())
check("nokta: ic ice dizin yok", not (t / "nokta").exists())
check("nokta: baslik dizinin adi", (t / "nokta-impl/CLAUDE.md").read_text().startswith("# nokta\n"))
t = WORK / "nokta-dolu" / "dolu"; t.mkdir(parents=True); (t / "notlar.md").write_text("x\n")
out, code = devenv(t, "create", ".", "--lang", "go", answer="n")
check("nokta dolu N: soruldu, dokunulmadi", "ezeyim mi" in out and not ok(code) and not (t / "dolu-impl").exists())
out, code = devenv(t, "create", ".", "--lang", "go", answer="y")
check("nokta dolu y: kuruldu, dosya silinmedi", ok(code) and (t / "dolu-impl/.git").is_dir() and (t / "notlar.md").is_file())

# reddedilenler
t = WORK / "red"; (t / "repo").mkdir(parents=True); git_init(t / "repo")
out, code = devenv(t, "create", "repo", "--lang", "go")
check("red: ust dizin repo ise", not ok(code) and "ust dizin repo olamaz" in str(code))
out, code = devenv(t, "go")
check("red: alt komutsuz cagri", not ok(code))
out, code = devenv(t, "create", "x/y", "--lang", "go")
check("red: adda '/'", not ok(code))
out, code = devenv(t, "create", "ornek", "go")
check("red: dil -l'siz", not ok(code))

m = load()
check("tilde: home altinda ~", m.tilde(Path.home() / ".config/claude") == "~/.config/claude")
check("tilde: disarida mutlak", m.tilde(Path("/tmp/x")) == "/tmp/x")

if all(results):
    shutil.rmtree(WORK)
    print(f"\n{len(results)}/{len(results)} gecti")
else:
    print(f"\n{sum(results)}/{len(results)} gecti; incelemek icin: {WORK}")
sys.exit(0 if all(results) else 1)
