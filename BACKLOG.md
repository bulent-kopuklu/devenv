# Backlog

Açık işler. Kapananlar silinir. Harita ve ilkeler `CLAUDE.md`'de.

## Şablon (yeni projeler için)

- [ ] Anayasa şablonuna (`templates/speckit/constitution.md`) güvenlik ilkesi.
      Kullanıcı onayladı. Metin:
      "Güvenlik tasarımında önce standart desen aranır. Kendini ispatlamış bir
      çözüm varsa o kullanılır: RFC ya da yayımlanmış bir standart, yaygın ve
      bakımlı bir kütüphane, bilinen bir protokol. Özel çözüm ancak adayların
      incelenip neden yetmediğinin kaynakla yazılmasından sonra tasarlanır.
      Kripto primitifi ve protokol kendimiz yazılmaz. Kanıt biçimi: güvenlik
      kararı, incelenen adaylar ve kaynaklarıyla research.md'de durur."
      Şablonun ilke numaralamasına ve sürüm kaydına uy.
- [ ] CLAUDE.md şablonuna (`templates/claude/CLAUDE.md`) `doc/` kuralı.
      Kullanıcı onayladı. Metin: "`doc/` yalnız insan içindir. Ajan oraya
      istendiğinde yazar ve düzenlerken okuyabilir. Ama `doc/` otorite değildir:
      oturum açılışında okunmaz; spec, plan, tasks ve kod ona dayanmaz ve
      referans vermez. `doc/` ile spec/plan çelişirse spec/plan esastır, `doc/`
      güncellenir." `doc/` kökte izinli dizinler listesine girer.
- [ ] CLAUDE.md şablonu `flake.nix`'i yalnız devshell olarak anlatıyor. Proje
      flake'ten release paketi de çıkarıyorsa `make dist` ölü ama doğru görünen
      ikinci bir yol olur; şablon bunu söylemeli.
- [ ] `devenv` CLAUDE.md'deki `Diller: LANGS` satırını doldurmuyor.
- [ ] Makefile: yalnız kütüphane içeren bir Go modülünde `make build` "go: no
      main packages to build" veriyor (`go build -o $(BIN)/ ./...` main paketi
      bulamıyor). Düzeltme: önce `go build ./...`, sonra `-o` yalnız
      `go list` ile bulunan main paketlerine.
- [ ] Makefile: Go cross build devshell'in içinde çalışmıyor. Devshell `CC=gcc`
      export ediyor (nix stdenv); `CC` tanımlıyken Go cross derlemede cgo'yu
      açıyor ve host gcc'si hedef assembly'yi derleyemiyor. Düzeltme: cross
      hedeflerde `CGO_ENABLED=0`. Şablonun cross testi devshell'in içinde
      yapılmalı; önceki test dışında yapıldığı için hatayı görmedi.
- [ ] Makefile: node bileşeninin çıktısı bileşenin içinde kalıyor, `dist`'e
      girmiyor. Gradle (java, android) sürülmüyor; öyle bir bileşen "manifest
      yok" hatası verir.
- [ ] Base `.gitignore`'da `__pycache__/` yok. `build-pipeline.py`
      `.specify/extensions/companion/scripts/__pycache__/` bırakıyor ve kurulum
      commit'ine `.pyc` giriyor.
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
