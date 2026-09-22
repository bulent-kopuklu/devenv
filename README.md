# dev-templates

Project scaffolding: the `devenv` command, `nix flake init` templates and a
devshell library.

## Install

```bash
./install.sh              # everything
NO_PI=1 ./install.sh      # skip the git-server side
```

It copies, it does not symlink: `bin/` → `~/.local/bin`, `templates/` →
`~/.local/share/devenv/templates`, `claude/` → the Claude config directory,
`pi/` → the git server. Run it again after pulling. `devenv --version` prints
the version and the commit the install came from.

## `devenv create`

```bash
devenv create ornek -l go -l rust --speckit
devenv create . -l rust -l cpp --target aarch64
devenv create ornek -l node --node 22
```

| option | |
|---|---|
| `<name>` or `.` | project name; `.` takes the current directory as the project directory |
| `-l`, `--lang` | `rust` `cpp` `go` `node` `java` `android`, repeatable |
| `--target` | cross target: `aarch64` `armv7`, repeatable |
| `--node` | node major version for `.nvmrc` |
| `--speckit` | install Spec Kit into the product repo |

```
ornek/
├── CLAUDE.md
├── ornek-impl/        the product repo
└── ornek-ctrl/        the reviewer
```

If the directory is not empty it asks first (y/N). Nothing is committed and no
remote is added. Before the first step, in `ornek-impl`: add the remote, commit
the skeleton, `git push -u origin main`. Then start the two sessions:

```bash
cd ornek/ornek-impl && claude -n ornek-impl
cd ornek/ornek-ctrl && claude -n ornek-ctrl
```

## Makefile

Code lives under `components/<name>/`, one language per component; a new
component is a new directory. Gradle (java, android) is not driven.

```bash
make                                   # build, VARIANT=debug TARGET=host
make build VARIANT=release TARGET=aarch64
make test COMPONENTS="api agent"       # test is host-only
make build-agent                       # one component; also test-<name>, lint-<name>
make dist TARGET=armv7                 # release build → dist/armv7/
make gate                              # distclean, build, lint, test, test-integration
make clean                             # build/
make distclean                         # + dist/, components/*/{node_modules,target}
```

## `nix flake init` templates

```bash
nix flake init -t github:bulent-kopuklu/devenv#base            # flake.nix, .envrc, .gitignore
nix flake init -t github:bulent-kopuklu/devenv#cpp             # .clangd, .clang-format, .editorconfig
nix flake init -t github:bulent-kopuklu/devenv#rust            # rustfmt.toml
nix flake init -t github:bulent-kopuklu/devenv#go              # .golangci.yml
nix flake init -t github:bulent-kopuklu/devenv#node            # biome.json
nix flake init -t github:bulent-kopuklu/devenv#android-native  # cmake-android helper, VSCode cmake tasks
nix flake init -t github:bulent-kopuklu/devenv#claude          # CLAUDE.md
nix flake init -t github:bulent-kopuklu/devenv#shell           # shell.nix + .envrc when flake.nix cannot be committed
```

`nix flake init` never overwrites existing files. In the generated `flake.nix`
edit two lines:

```nix
langs = [ "rust" "cpp" ];   # rust cpp go node java android
targets = [ "aarch64" ];    # aarch64 armv7
```

`lib.mkEnv { pkgs, langs, targets, src, android }` returns
`{ packages, shellHook }`. A `rust-toolchain.toml` in `src` overrides the
default stable Rust (it must then list the cross targets itself). Node follows
`.nvmrc` / `.node-version`.

## Repos on the git server

```bash
git config --global url."git@git.kopuklu.io:/mnt/storage/workspace/git-repos/".insteadOf "git.kopuklu.io:"
newrepo nats-bridge                               # empty repo
newrepo nats-bridge git@gitlab:grup/repo.git      # prints fork-flow wiring: origin = server, upstream = company
```
