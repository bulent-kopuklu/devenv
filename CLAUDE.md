# dev-templates (devenv)

Bu repo iki şey dağıtır: `devenv` aracını ve Claude Code'un global
yapılandırmasının kaynağını. Kullanım `README.md`'de ve `devenv create --help`'te;
bu dosya repoyu geliştirene.

## Harita

| yol | ne | kurulunca nereye |
|---|---|---|
| `bin/devenv` | `devenv create <ad\|.> <diller> [--speckit]`: iki rollü proje | `~/.local/bin` |
| `bin/newrepo`, `pi/` | git sunucusunda repo açma | laptop, sunucu |
| `claude/CLAUDE.md` | kullanıcının global CLAUDE.md'si | `$CLAUDE_CONFIG_DIR/CLAUDE.md` |
| `claude/roles/` | rol metinleri: `protocol`, `ctrl`, `impl` | `$CLAUDE_CONFIG_DIR/roles/` |
| `claude/skills/` | global skill'ler (`spike`, `context: fork`) | `$CLAUDE_CONFIG_DIR/skills/` |
| `templates/` | projeye kopyalanan şablonlar; `project/` rol dizinlerinin yer tutuculu dosyaları | `~/.local/share/dev-templates/templates` |
| `lib/` | `lib.mkEnv`: projelerin `flake.nix`'inin kullandığı devshell kütüphanesi | flake input'u |
| `tests/` | `devenv create` senaryoları | — |

Kurulumu `install.sh` yapar ve kopyalar, symlink kurmaz. Bu makinede
`$CLAUDE_CONFIG_DIR` = `~/.config/claude`.

## Düzen

```
<ad>/            git değil; Claude burada çalışmaz; CLAUDE.md protokolü import eder
├── <ad>-impl/   ürün, tek git reposu (remote <ad>.git); yazan oturum
└── <ad>-ctrl/   denetçi; git değil; yalnız record.md'ye yazar, karar verir
```

## İlkeler

- **İki rol.** Yazan oturum kendi kararlarını denetleyemiyor: aynı oturumdaki
  hakem temiz hakemden 20 kararın 9–10'unda ayrıştı, iki temiz hakem arası 3–4
  (cc-workspace `docs/sdlc/yazan-hakem-bagimsizligi.md`). Ayrı dizin, rolü
  kendi CLAUDE.md'sinden ve hafızayı ayrı getirir.
- **Davranış metni tek yerde.** Rol metinleri ve skill'ler global'de; projeye
  yalnız projeye özgü olan (ad, yol, izin) üretilir. Güncelleme bir
  `install.sh`'tır, proje proje dolaşmak değil.
- **Ürün reposu kendi kendine yeter.** Commit'lenen `CLAUDE.md` ürüne aittir.
  Makineye özgü olan (rol import'u, mutlak yollu izinler) `CLAUDE.local.md` ve
  `.claude/settings.local.json`'da, `.git/info/exclude`'da.
- **Ad argümandan gelir**, dizin adından değil: `-impl` ürüne sızmaz.
- **Var olana dokunulmaz.** Var olan dosya korunur; izin JSON'unun listeleri
  birleştirilir. Kurulu `.specify/` varsa `--speckit` atlanır.
- **Orchestration kurulmaz.** Hakem ve `after_*` hook'ları kararı yazan
  oturumun içinde veriyordu; bu düzende karar denetçinindir.
- **Ürünsüz.** Şablonlara ve rol metinlerine hiçbir projenin adı, kararı ya da
  örneği girmez.
- **Adlar İngilizce, içerik Türkçe.** Dosya ve dizin adları İngilizcedir
  (`record.md`, `handoff.md`), metnin kendisi Türkçedir.

## Değişiklikten sonra

- `python3 -B tests/devenv_create.py`: yeni proje, ikinci koşu, var olan repoyu
  alma, `create .`, reddedilen çağrılar. Nix build'i atlar, geçici dizinde koşar.
- `install.sh`'i gerçek config'e dokunmadan dene:
  `CLAUDE_CONFIG_DIR=$(mktemp -d) BINDEST=$(mktemp -d) XDG_DATA_HOME=$(mktemp -d) NO_PI=1 ./install.sh`
- Gerçek `./install.sh` global config'i değiştirir: kullanıcının onayıyla.
- `python3 -m py_compile` kullanma: `bin/__pycache__` bırakır ve `install.sh`
  onu tool sanıp düşer.
- `VERSION` elle artırılır; komut satırı geriye uyumsuz değişirse major.

## Açık işler

`BACKLOG.md`.
