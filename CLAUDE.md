# dev-templates (devenv)

Bu repo iki şey dağıtır: `devenv` aracını ve Claude Code'un global
yapılandırmasının kaynağını. Kullanım `README.md`'de ve `devenv create --help`'te;
bu dosya repoyu geliştirene.

## Harita

| yol | ne | kurulunca nereye |
|---|---|---|
| `bin/devenv` | `devenv create <ad\|.> -l <dil>... [--speckit]`: proje; `--speckit` ile iki rollü. `devenv add -l <dil>...`: var olan projeye dil | `~/.local/bin` |
| `bin/newrepo`, `pi/` | git sunucusunda repo açma | laptop, sunucu |
| `claude/CLAUDE.md` | kullanıcının global CLAUDE.md'si | `$CLAUDE_CONFIG_DIR/CLAUDE.md` |
| `claude/skills/` | global skill'ler (`spike`, `context: fork`) | `$CLAUDE_CONFIG_DIR/skills/` |
| `templates/` | projeye kopyalanan şablonlar; `claude/CLAUDE.md` `--speckit`'siz projenin CLAUDE.md'si; `speckit/` yalnız `--speckit`'in yazdıkları: `project/` üst dizinin ve rol dizinlerinin dosyaları (rol metni, impl'in yerleşim ve Makefile sözleşmesi `.claude/rules/`'da), `constitution.md` her projenin anayasası (araç ve rol adı taşımaz) | `~/.local/share/devenv/templates` |
| `lib/` | `lib.mkEnv`: projelerin `flake.nix`'inin kullandığı devshell kütüphanesi | flake input'u |
| `tests/` | `devenv create` senaryoları | — |

Kurulumu `install.sh` yapar ve kopyalar, symlink kurmaz. Bu makinede
`$CLAUDE_CONFIG_DIR` = `~/.config/claude`.

## Düzen

`--speckit`'siz proje dizini ürün reposudur:

```
<ad>/            ürün, tek git reposu; tek oturum
```

`--speckit` ile:

```
<ad>/            git değil; Claude burada çalışmaz; CLAUDE.md protokolü import eder
├── <ad>-impl/   ürün, tek git reposu (remote <ad>.git); yazan oturum
└── <ad>-ctrl/   denetçi; git değil; yalnız kendi dizinine yazar (work/,
                 reference/), karar verir
```

## İlkeler

- **İki rol (`--speckit`).** Yazan oturum kendi kararlarını denetleyemiyor: aynı oturumdaki
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
- **create yalnız yaratır.** Ad `.` ise bulunulan dizinin adı, değilse
  argümandır; sonrası tek yol. Proje dizini doluysa önce sorar (y/N); y ise
  şablon dosyalarını var olanların üstüne yazar, hiçbir şey silmez. Var olanı
  koruma, izin birleştirme, repo alma yoktur; o iş ayrı bir komutundur.
- **Dil eklemek `add`'in işidir.** Var olan dosyaya dokunmaz; Makefile'a,
  `CLAUDE.md`'ye, Spec Kit'e ve rol dosyalarına dokunmaz.
- **Kök Makefile dilsiz bir iskelettir.** Arayüzü (hedefler, parametreler,
  çıktı yeri) taşır, reçete taşımaz; bir hedefi bileşenlerin kendi
  Makefile'larına, evidence hedeflerini yine dilsiz olan `evidence/Makefile`'a
  indirir. Bileşenin ve evidence dizininin Makefile'ını onu açan agent yazar;
  bileşen ya da evidence dizini eklemek kökü değiştirmez. Bir dilin reçete bilgisi (bayraklar,
  cross) o dilin `rules.md`'sindeki Makefile bölümündedir.
- **Orchestration kurulmaz.** Hakem ve `after_*` hook'ları kararı yazan
  oturumun içinde veriyordu; bu düzende karar denetçinindir.
- **Ürünsüz.** Şablonlara ve rol metinlerine hiçbir projenin adı, kararı ya da
  örneği girmez.
- **Adlar İngilizce, içerik Türkçe.** Dosya ve dizin adları İngilizcedir
  (`work/`, `reference/`), metnin kendisi Türkçedir.

## Değişiklikten sonra

- `python3 -B tests/devenv_create.py`: yeni proje `--speckit`'li ve
  `--speckit`'siz, dolu dizinde N ve y, `create .` boş ve dolu, go projesine
  `add` ile rust, reddedilen çağrılar. Nix build'i atlar, geçici dizinde
  koşar.
- `templates/make/Makefile` değişirse boş bir dizinde her hedefi ve geçersiz
  `VARIANT`/`TARGET`'ı koş. Bir dilin `rules.md`'sindeki Makefile bölümü
  değişirse reçeteyi bir devshell'in içinde, cross hedefle birlikte dene. Devshell `CC`'yi export eder; dışında görünmeyen hatalar
  içinde çıkar. Değişiklikten önceki Makefile'ı aynı düzenekte koş: hatayı
  gösteremeyen deneme düzeltmeyi de kanıtlamaz.
- `install.sh`'i gerçek config'e dokunmadan dene:
  `CLAUDE_CONFIG_DIR=$(mktemp -d) BINDEST=$(mktemp -d) XDG_DATA_HOME=$(mktemp -d) NO_PI=1 ./install.sh`
- Gerçek `./install.sh` global config'i değiştirir: kullanıcının onayıyla.
- `python3 -m py_compile` kullanma: `bin/__pycache__` bırakır ve `install.sh`
  onu tool sanıp düşer.
- `VERSION` elle artırılır; komut satırı geriye uyumsuz değişirse major.
