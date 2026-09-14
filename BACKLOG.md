# Backlog

Açık işler. Kapananlar silinir. Harita ve ilkeler `CLAUDE.md`'de.

## Tasarım (konuşuldu, uygulanmadı)

- [ ] **Proje ağacı plandan sonra belirlenir.** Bugün iki yerden dayatılıyor:
      CLAUDE.md şablonunun `## Yerleşim`'i (`components/<ad>/` zorunlu; her
      oturumda yüklü olduğu için stock `/speckit-plan`'ı da bağlar) ve plan-doc
      node'u (Companion'ın orijinalinden tek farkı "layout is already decided"
      cümlesi). Spec Kit'in plan şablonunda kararın yeri zaten var: Project
      Structure ve "Structure Decision".
  - Baştan kalanlar, dil sayısından bağımsız ilkeler: üretim, kurulum
    (`install/`) ve ölçüm (`proof/`) kodu ayrı dizinlerde (anayasa III);
    sözleşme kendi biriminde, kodunu tüketici üretir; köke rastgele dizin
    açılmaz. Bir de kökte `make build`, `make lint`, `make test` sözleşmesi
    (GitLab CI maddesi).
  - Plandan sonra karar verilenler: ağaç (`components/` ve dağıtıcı Makefile
    ya da dilin kendi ağacı ve ince bir Makefile), dil listesi, cross için
    gereken (tek dilli C++'ta `CMakePresets.json`). Ölçüt dil sayısı değil,
    kökten sürülen ayrı build aracı sayısı: Go ve proto tek araçtır
    (`go generate`); `proof/`'taki Python make'e girmez.
  - Karar anı plan ile tasks arası, ctrl'in plan turunda: tasks yolları yazar,
    ağaç sonra değişirse tasks baştan yazılır. ctrl önerir, insan onaylar,
    `record.md`'ye girer.
  - ctrl'e bir skill: ölçüt, iki ağaç, cross notu, karardan sonra impl'in
    güncelleyecekleri. ctrl.md'ye değil skill'e, çünkü proje başına bir kez
    lazım. `context: fork` değil, çünkü karar ctrl'in context'inde verilir.
    impl'de yasak.
  - Mekanik kısım devenv'de (`devenv update`'in parçası): seçilen dillerle
    Makefile ve Yerleşim bölümü. Seçilmeyen dilin satırları Makefile'a girmez;
    o dilde bir bileşen "bu projede seçili değil, `flake.nix` langs'e ekle"
    hatası alır. impl elle yalnız plan.md'nin Proje Yapısı'nı ve `flake.nix`
    dillerini (insan onayıyla) günceller.
  - Sonuçları: `create` `components/` kuralını koymaz; plan-doc replacement'ı
    gider; Companion'ı klondan (`--dev`) kurma gereği muhtemelen gider (build
    toolchain'ini başka kullanan var mı, bakılır).
- [ ] **GitLab CI.** Ekip GitLab CI kullanıyor; projeler bir noktadan sonra
      CI'ya bağlanacak.
  - Kapı tek yerde tanımlı: CI, ajan ve insan aynı `make` hedeflerini çağırır;
    `.gitlab-ci.yml` komut tekrarlamaz.
  - CI'da toolchain devshell'den gelir; gelmezse yerelde yeşil olan CI'da
    sürüm farkından kırmızı yanar. İki aday: Nix'li runner'da
    `nix develop -c make …`, ya da flake'ten (`lib.mkEnv`'in `packages`'ı)
    üretilip GitLab registry'de duran bir image. Seçim ekibin runner'larına
    bağlı; ekibe sorulur.
  - Her push'ta tam koşu yok. Uzun koşular (lab'a muhtaç kanıt kapıları,
    bütün case'ler; gerçek bir projede hazırlık ve koşu yarım günü aşıyor)
    zamanlanmış ya da elle tetiklenir. Push'ta yalnız hızlı kapı (build, lint,
    birim test) mı koşar, hiç mi koşmaz: ekibin kararı. GitLab'ın hangi
    mekanizmasıyla (schedule, manual job, `rules`) yapılacağı tasarımda
    kaynakla seçilir.
  - devenv'in payı: CI image'ı için bir flake çıktısı ve make hedeflerini
    çağıran bir `.gitlab-ci.yml` iskeleti. İkisi ağaca değil make sözleşmesine
    bağlı; `create` anında verilebilir.
  - İki rollü akışta: CI insan onaylı push'tan sonra koşar, ekibin kapısıdır.
    Ajanların kapısı yerel `make`; pipeline sonucu ctrl için ek kanıttır.

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
      Tasarım'daki ağaç maddesi uygulanırsa bu madde düşer.
- [ ] `~/workspace/ai-rules/rust.md` kuralın ikinci kopyası; tek kaynak
      `templates/rules/`.

## Rol metinleri

- [ ] Canlıda doğrulanmadı: dış import'un onay penceresi, `/context`'te rol
      metninin görünmesi, impl'de `Skill(spike)` yasağının ve ctrl'de impl'e
      Edit yasağının tuttuğu. İlk pilot projede bakılır.
      2026-09-14, dbaas'ta `claude -p` ile görülen: onaysız dizinde dış
      import açılmıyor, model yalnız `@~/...` satırını görüyor. Onay proje
      başına `.claude.json`'da (`hasClaudeMdExternalIncludesApproved`).
      ctrl'ün `.claude/settings.json`'daki `additionalDirectories`'i trust
      verilmemiş dizinde yok sayılıyor. impl'in `settings.local.json`'u için
      bu uyarı çıkmadı. Her dizin bir kez etkileşimli açılıp iki onay
      verilmeli; bunu `devenv create` çıktısı ve README söylemeli.
- [ ] Kaynak kapısı için araç: oturumun transcript'inden context doluluğunu
      okuyan küçük bir script. Rol metni "doluluk transcript'teki son
      `usage`'dan okunur" diyor, ama okuyan bir araç yok.
