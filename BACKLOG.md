# Backlog

Açık işler. Kapananlar silinir. Harita ve ilkeler `CLAUDE.md`'de.

## Şablon (yeni projeler için)

- [ ] CLAUDE.md şablonu `flake.nix`'i yalnız devshell olarak anlatıyor. Proje
      flake'ten release paketi de çıkarıyorsa `make dist` ölü ama doğru görünen
      ikinci bir yol olur; şablon bunu söylemeli.
- [ ] `devenv` CLAUDE.md'deki `Diller: LANGS` satırını doldurmuyor.
- [ ] Makefile: node bileşeninin çıktısı `dist`'e girmiyor; Makefile'ın
      başında yazılı. Toplamak için bir çıktı dizini sözleşmesi gerekiyor
      (`dist/`, `build/`, framework'e göre değişiyor); ilk gerçek node
      bileşeninde karar verilir. Gradle (java, android) sürülmüyor; öyle bir
      bileşen "manifest yok" hatası verir.
- [ ] Makefile: `go_test` ve `go_lint` `go generate` koşmuyor. Üretilen kod
      commit'lenmiyorsa temiz ağaçta `make test` ve `make lint`, `make`'ten önce
      koşulunca düşer. Gerçek bir projede aynı düzeltme yapıldı.
- [ ] `lib.mkEnv` Rust toolchain'ini de döndürsün. Release paketini flake'ten
      derleyen bir proje bugün toolchain'e devenv'in iç input'u
      (`rust-overlay`) üzerinden uzanıyor; devshell `rust-toolchain.toml`
      varsa aynı toolchain'i kullanmalı.

## devenv

- [ ] `devenv update`: kurulu bir projeyi güncel şablona getirir; eksik
      dosyaları ekler, izin listelerini birleştirir.
- [ ] Exclude satırları köke bağlı değil: `.gitignore` satırı projedeki bütün
      `.gitignore`'ları gizliyor, Spec Kit'in `.specify/.gitignore`'u dahil.
      Projeye ait olanlar (`CLAUDE.md`, `.claude/rules/`, `.gitignore`,
      formatter/linter config'leri) `flake.nix` gibi intent-to-add edilmeli;
      exclude'da yalnız kişisel olanlar kalmalı ve `/` ile köke bağlanmalı.
      Bugün clone'layan kişi yerleşim kuralını, dil kurallarını, lint ayarını
      almıyor.
- [ ] Dil kuralları (`templates/rules/<dil>.md`) projeye kopyalanıyor:
      güncellemede proje proje dolaşma sorunu. Ama ürün reposu başka makinede
      de kendi kendine yetmeli. Karar gerekiyor.
- [ ] Companion'ın `companion-standard` preset'i kurulmuyor. VS Code eklentisi
      proje ilk açıldığında sormadan kuruyor ve 7 stock `speckit-*` skill'ini
      değiştiriyor; proje durumu editörle açılıp açılmamasına bağlı kalıyor.
      `specify preset add --dev <companion>/presets/companion-standard`.
- [ ] Extension kurulurken kaynağın `.git`'i de kopyalanıyordu (gömülü repo,
      gitlink). Bugün yalnız Companion kuruluyor, URL'den klonlanarak; hâlâ
      oluyor mu bakılmalı.
- [ ] Repo adı `devenv`, iç adlar hâlâ `dev-templates`: yerel dizin,
      `~/.local/share/dev-templates`, `DEV_TEMPLATES_REF`, flake input adı.
- [ ] README'deki "Claude Code skill" bölümü `skills/devenv`'i anlatıyor; repoda
      böyle bir dizin yok.
- [ ] `SPECKIT_INTEGRATION_CLAUDE_EXTRA_ARGS` kuruluma girmiyor; koşuyu başlatma
      biçimi README'de durmalı.
- [ ] `plan-doc` replacement'ı plan'ı `components/<ad>/` altına yazdırıyor mu,
      gerçek koşuda görülmedi. Replacement yalnız Companion komutlarında
      devrede; stock `/speckit-plan` Spec Kit'in `src/` varsayılanıyla geliyor.
- [ ] `~/workspace/ai-rules/rust.md` kuralın ikinci kopyası; tek kaynak
      `templates/rules/`.

## Rol metinleri

- [ ] Canlıda doğrulanmadı: dış import'un onay penceresi, `/context`'te rol
      metninin görünmesi, impl'de `Skill(spike)` yasağının ve ctrl'de impl'e
      Edit yasağının tuttuğu. İlk pilot projede bakılır.
- [ ] Kaynak kapısı için araç: oturumun transcript'inden context doluluğunu
      okuyan küçük bir script. Rol metni "doluluk transcript'teki son
      `usage`'dan okunur" diyor, ama okuyan bir araç yok.
