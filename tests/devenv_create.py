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


def devenv(cwd, *argv):
    os.chdir(cwd)
    m = load()
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
out, code = devenv(t, "create", "ornek", "go", "--speckit")
root, impl, ctrl = t / "ornek", t / "ornek/ornek-impl", t / "ornek/ornek-ctrl"
check("yeni: cikis 0", ok(code))
check("yeni: ust dizin repo degil", not (root / ".git").exists())
check("yeni: impl repo, ctrl degil", (impl / ".git").is_dir() and not (ctrl / ".git").exists())
check("yeni: ust CLAUDE.md protokolu import eder", f"@{CFG}/roles/protocol.md" in (root / "CLAUDE.md").read_text())
check("yeni: ctrl CLAUDE.md rolu import eder", f"@{CFG}/roles/ctrl.md" in (ctrl / "CLAUDE.md").read_text())
check("yeni: ctrl record.md, uc bolum", (ctrl / "record.md").read_text().count("\n## ") == 3)
check("yeni: impl CLAUDE.local.md rolu import eder", f"@{CFG}/roles/impl.md" in (impl / "CLAUDE.local.md").read_text())
check("yeni: baslik proje adi, dizin adi degil", (impl / "CLAUDE.md").read_text().startswith("# ornek\n"))
check("yeni: yer tutucu kalmadi", not any(re.search(r"\{\{[A-Z]+\}\}", p.read_text()) for p in root.rglob("*")
                                         if p.is_file() and ".git" not in p.parts))
check("yeni: speckit cagrildi", "[speckit]" in out)
check("yeni: oturum komutlari basildi", "claude -n ornek-impl" in out and "claude -n ornek-ctrl" in out)
cs, ls = settings(ctrl / ".claude/settings.json"), settings(impl / ".claude/settings.local.json")
check("yeni: ctrl impl'e yazamaz", f"Edit(/{impl}/**)" in cs["deny"] and cs["deny"][0].startswith("Edit(//"))
check("yeni: ctrl impl'i ve wiki'yi okur", str(impl) in cs["additionalDirectories"] and len(cs["additionalDirectories"]) == 2)
check("yeni: impl ctrl'e yazamaz, CLAUDE.md'sini okuyamaz",
      f"Edit(/{ctrl}/**)" in ls["deny"] and f"Read(/{ctrl}/CLAUDE.md)" in ls["deny"])
check("yeni: impl spike cagiramaz", "Skill(spike)" in ls["deny"] and "Skill(spike *)" in ls["deny"])
excl = (impl / ".git/info/exclude").read_text()
check("yeni: yerel dosyalar exclude'da",
      all(f in excl for f in ("CLAUDE.local.md", ".claude/settings.local.json", "handoff.md")))
status = subprocess.run(["git", "-C", str(impl), "status", "--porcelain"], capture_output=True, text=True).stdout
check("yeni: yerel dosyalar git status'ta yok", "CLAUDE.local.md" not in status and "settings.local" not in status)

# ikinci kosu
out, code = devenv(t, "create", "ornek", "go")
check("ikinci: cikis 0", ok(code))
check("ikinci: yeni dosya yok", "created:" not in out)
check("ikinci: exclude tekrarlanmadi", (impl / ".git/info/exclude").read_text().count("CLAUDE.local.md") == 1)

# var olan repoyu alma
t = WORK / "alma"; impl2 = t / "eski/eski-impl"; impl2.mkdir(parents=True)
git_init(impl2)
(impl2 / "CLAUDE.md").write_text("# eski\n\nmevcut\n")
(impl2 / ".specify").mkdir()
(impl2 / ".claude").mkdir()
(impl2 / ".claude/settings.local.json").write_text(
    json.dumps({"permissions": {"allow": ["Bash(ls)"], "deny": ["Read(./.env)"]}}))
out, code = devenv(t / "eski", "create", ".", "go", "--speckit")
s = settings(impl2 / ".claude/settings.local.json")
check("alma: cikis 0", ok(code))
check("alma: CLAUDE.md korundu", (impl2 / "CLAUDE.md").read_text() == "# eski\n\nmevcut\n")
check("alma: izinler birlesti", "Bash(ls)" in s["allow"] and "Read(./.env)" in s["deny"] and "Skill(spike)" in s["deny"])
check("alma: kurulu Spec Kit ezilmedi", "atlandi: speckit" in out and "[speckit]" not in out)

# create . : bulunulan dizin proje dizini
t = WORK / "nokta" / "nokta"; t.mkdir(parents=True)
out, code = devenv(t, "create", ".", "go")
check("nokta: cikis 0", ok(code))
check("nokta: impl ve ctrl bulunulan dizinde", (t / "nokta-impl/.git").is_dir() and (t / "nokta-ctrl/record.md").is_file())
check("nokta: ic ice dizin yok", not (t / "nokta").exists())
check("nokta: baslik dizinin adi", (t / "nokta-impl/CLAUDE.md").read_text().startswith("# nokta\n"))

# reddedilenler
t = WORK / "red"; (t / "repo").mkdir(parents=True); git_init(t / "repo")
out, code = devenv(t, "create", "repo", "go")
check("red: ust dizin repo ise", not ok(code) and "ust dizin repo olamaz" in str(code))
out, code = devenv(t, "go")
check("red: alt komutsuz cagri", not ok(code))
out, code = devenv(t, "create", "x/y", "go")
check("red: adda '/'", not ok(code))

m = load()
check("tilde: home altinda ~", m.tilde(Path.home() / ".config/claude") == "~/.config/claude")
check("tilde: disarida mutlak", m.tilde(Path("/tmp/x")) == "/tmp/x")

if all(results):
    shutil.rmtree(WORK)
    print(f"\n{len(results)}/{len(results)} gecti")
else:
    print(f"\n{sum(results)}/{len(results)} gecti; incelemek icin: {WORK}")
sys.exit(0 if all(results) else 1)
