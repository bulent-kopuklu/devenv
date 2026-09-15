# Backlog

Açık işler. Kapananlar silinir. Harita ve ilkeler `CLAUDE.md`'de.

## İki rollü akış (konuşuldu 2026-09-15)

Kararlar değişebilir. `claude/roles/` bunlara göre baştan yazıldı; aşağıdaki
açık maddeler metinde `AÇIK` diye duruyor. Kaynak okumaları cc-workspace'te:
`docs/sdlc/speckit-komutlari.md`, `companion-komutlari.md`,
`speckit-hook-duzlemleri.md`.

### Kararlar

- [ ] **Amaç.** devenv geliştirme ortamını kurar; geliştirme proje dizininde
      spec-kit ve Companion ile yapılır. `devenv create` ile yaratılan
      projede her şey hazır olmalı. Yeni dil ekleme belki sonra.
- [x] **Roller.** Çalışan her şey impl'in üstünde: komutları koşar, kodu
      yazar. ctrl tarafsız denetçidir ve bir sonraki adımı başlatır; biten
      her işi kontrol eder, itirazını söyler, gelen soruları cevaplar.
      Disiplin impl'deki spec-kit'te.
- [x] **Komutlar.** specify, clarify, plan, tasks, analyze stock
      `/speckit-*`: elle koşulunca adım sonunda duruyor. Companion komutları
      kendi kendine sonraki adıma geçiyor (self-advance) ve bunu kapatan bir
      ayar yok. implement `/speckit-companion-implement` ile (kullanıcı
      önerdi, "mahsuru yoksa"); ondan sonra başlatılacak adım yok.
      Companion'ın `after_*` hook'ları stock komutlarda da çalışıyor, panel
      ve kayıt sürüyor. Workflow motoru (`specify workflow run`) kullanılmaz:
      her adım `claude -p`, adımın ortasındaki soruyu kimse cevaplamaz, soru
      sorup biten adım başarılı sayılır.
- [x] **Akış.**
  - ctrl spec girdisini hazırlar (bkz. Spec girdisi).
  - impl specify'ı koşar. ctrl spec'i kendi kopyasıyla karşılaştırır: her
    madde girmiş mi, Assumptions'ta sessiz karar var mı. İtiraz varsa spec
    o anda değiştirilir.
  - impl plan'ı ctrl'in prompt'uyla koşar. ctrl planın tamamını,
    `research.md`'deki kararlar dahil, kontrol eder; itiraz varsa plan o
    anda değiştirilir.
  - impl tasks'ı koşar; tasks bitince ctrl analyze'ı koşar; sonra
    implement. implement'ten sonrası konuşulmadı.
- [x] **Sorular.** impl her adımda, kararsız kaldığı her yerde soru
      sorabilir; akış soruların belli noktalarda geleceğine dayanmaz. impl
      soruyu bağlamıyla ctrl'e iletir, ctrl cevaplar. Plan sonundaki "şu
      soruları cevapla, onaylıyor musun" bütün planın onayıdır; ctrl onu
      planın tamamını inceleyerek verir.
- [x] **Plan'a müdahale: önden cevap ve sonra kontrol.** Research plan'ın
      içinde (Phase 0); araya girilecek bir durak yok. ctrl bildiği büyük
      kararları plan prompt'una yazar, plan bitince kontrol eder. İki
      adımlı plan ("Technical Context'ten sonra dur") ancak çevrilen
      research kararı çok çıkarsa denenir.
- [x] **analyze'ı ctrl koşar.** Salt okunur, subagent açmıyor, script'i
      yazmıyor; impl koşsa yazan kendi işini denetlemiş olur. ctrl impl'deki
      `.claude/skills/speckit-analyze/SKILL.md`'yi okuyup impl'in feature
      dizinine uygular; bulgular impl'e itiraz olarak gider.
- [x] **ctrl'in cevap yolu, maliyete göre.** Bilmediği soruda önce wiki;
      özellik sorusuysa referans projelerin ne yaptığı; teknoloji seçimiyse
      web search yetiyorsa o, yetmiyorsa spike. Sonucu görüp karar verir.
- [x] **Subagent.** ctrl subagent açmaz. Spike `context: fork` ile açılır,
      bu kabul; fork kendi içinde ajan açmaz. Kural impl için geçerli değil:
      spec-kit ve Companion kendi ajanlarını kullanır, limiti tükettikleri
      görülmedi. Ajan kuralı ctrl'in kuralıdır, impl'in gördüğü yerlerde
      (protocol, impl.md) durmaz.
- [x] **impl stock kalır.** Oraya yapılan her müdahale upgrade'in önünde
      engel. impl hiçbir şeye zorlanmaz; stock plan'ın research'ü ne
      yapıyorsa yapsın, bizi ilgilendirmiyor.
- [x] **Ürün soruları ctrl cevaplar.** Referans ürünlerden yararlanır;
      roadmap hazırlanırken bir referans ürün seçilir.
- [x] **Devir.** Bağlam dolunca insan compact ya da clear yapar. impl'in
      devir notu yok, önemi olmamalı: hazır belgeden gider.
- [x] **impl dışarı gitmez.** ctrl'in dizinini okumaz ve yazmaz; yüklediği
      dosyalarda (`CLAUDE.local.md`, üst dizinin `CLAUDE.md`'si) ctrl'in yolu
      ve `record.md`'si yok, yalnız ctrl'in oturum adı. Wiki global kuraldır,
      bu kararın dışında.
- [x] **impl'in gördüğü metin yalnız yönlendirme.** protocol.md ve impl.md'de
      yalnız komutlar, adımı kimin başlattığı, sorunun ve itirazın yolu,
      yazma alanı. ctrl'in kuralları, gerekçeler ve açık maddeler ctrl.md'de.
      impl'e spec-kit'in üstüne kural konmaz; rol metni context'i zehirleyebilir.
- [x] **Plan varsayılan ağacı kullanmaz.** Yerleşim README'deki "Layout and
      the root Makefile" ve `CLAUDE.md`'nin `## Yerleşim`'i. ctrl bunu
      plan'ı başlatırken prompt'la verir ya da plan bitince "burayı şöyle
      değiştir" der; node replacement ile değil. Plan anında dizin
      yaratılmaz, yalnız `plan.md` değişir; tasks yolları `plan.md`'den alır.
- [x] **Living spec başta kapalı.** İlk versiyondan sonra elle açılır
      (`living-specs.yml`'de `enabled: true`, sonra living-adopt). Stock
      specify ve plan living spec yüklemez; yükleme yalnız
      `speckit-companion-*` komutlarında. implement Companion ile olursa
      delta ve fold'u o yapar.
- [x] **Spec girdisi.** Sen kısıtları ve amacı verirsin; ctrl rakipleri
      web'den inceler; olmazsa olmaz özelliklerde mutabık kalınır.
  - Bütün projeyi bağlayan kurallar, platform kısıtları dahil, anayasaya
    girer (`/speckit-constitution`, impl'de). specify teknik detayı spec'ten
    siler, o yüzden spec girdisine konmazlar. Neyin anayasaya gireceğini
    bilmek için ctrl spec-kit'in davranışını iyi bilmeli.
  - Roadmap ctrl'le birlikte hazırlanır, ctrl'in dizininde durur, impl'e
    girmez. Dilim başına: amaç, kapsam ve kapsam dışı, bağımlılık, durum,
    spec yolu.
  - Her dilim ayrı bir specify'dır. Girdi dosya değil prompt olarak verilir,
    kapsam sınırı prompt'ta yazar; ctrl kopyasını kendi dizininde tutar.
    Prompt çerçeveyi taşır: "her madde girsin; atılanı adıyla ve
    gerekçesiyle yaz; adları değiştirme".
- [x] **ctrl davranışı sürüme göre.** Rol metninde amaç sabit; spec-kit
      davranışı kopyalanmaz, kurulu komut metninden okunur. İlk fazda ctrl
      şu an kurulu sürüme göre hazırlanır. `/ctrl-upgrade` (proje skill'i,
      global değil) ve davranış kartının yeri sonraki faz; projelerin
      spec-kit sürümleri farklı olabilir.
- [ ] **Roadmap nasıl hazırlanır.** Rol metnine henüz girmedi.
  1. ctrl seninle konuşur: ne yapıyoruz, kimin için, mecbur kullanacağımız
     teknoloji ve kısıt var mı. "Bu iş yapılır mı, kime hitap ediyor"
     sorulmaz.
  2. ctrl bu işi yapanları araştırır, ürünleri linkleriyle listeler. Sen 1,
     belki 2 ürünü referans seçersin.
  3. Referansların bütün özellikleri çıkarılır: nasıl çalıştıkları, neyi
     nasıl çözdükleri, bulunan her şey. Ölçüt: sonraki işlerde yine arama
     yapıyorsak eksik yapılmış.
  4. Özellikler birbirine bağımlı. ctrl, spec-kit'in user story mantığıyla
     7-8 parçalık bir öneri listesi hazırlar.
  5. Onayından sonra yalnız sıradaki parçanın spec'i hazırlanır; hepsinin
     değil. Plan ve araştırma sonucu kapsam kayabilir: 2. parçaya bırakılan
     bir şeyi 1. parçada yapmak gerekebilir.
  - Araştırma ctrl'in dizininde durur, wiki'ye yazılmaz: wiki oturmadı,
    wiki'ye yazan oturum 10 dakika sonra yazdığının tersini yapıyor.
  - Biçim belki global bir skill. Örnek: claude-forge'un `/product`'ı
    ("önce liste, onay, sonra analiz"; bulgu URL'li, yorum ayrı); müşteri
    ve pazar kısmı alınmaz.
- [ ] **Güvenlik kararları, ctrl'in kuralı.** Güvenlikle ilgili her karar web
      search'e dayanır. 2026'da çözülmemiş bir şey yapmıyoruz; kendi
      kendimize çözüm uydurmayız, neredeyse her şeyin deseni var. Referans
      araştırmasında ve plan kontrolünde güvenlik çözümlerine özellikle
      odaklanılır. Rol metnine henüz girmedi.

### Açık

- [ ] Wiki'ye yazmama kararının kapsamı. Spike'ın metni "yalnız wiki'ye
      yazarsın", ctrl'in cevap yolu "önce wiki" diyor; bunlar da mı? Global
      `CLAUDE.md` wiki yazımını "sorulmaz, tetiklenir" diye kuruyor ve ctrl
      onu yüklüyor; karar ctrl.md'de açıkça yazmazsa tutmaz.
- [ ] Bir parça bir spec mi? Parçanın içindeki user story'leri specify mı
      çıkarır; parça listesi user story mantığıyla mı kurulur (bağımsız test
      edilebilir, önceliği belli, öncekine dayanan)?
- [ ] Parçanın adı: "faz" mı, "dilim" mi? spec-kit'in `tasks.md`'sindeki
      "Phase"le karışabilir.
- [ ] Referans araştırmasının biçimi: global skill mi, adı, çıkarım
      dosyasının bölümleri, ctrl'in dizinindeki yeri.
- [ ] ctrl ile impl arasındaki mesajların biçimi.
- [ ] implement ve sonrası: commit, push, review, merge, insan onayı.
- [ ] Tek kaynak: impl'in dışarı gitmediği kesin. ctrl'in cevaplarının
      impl'deki belgelere (spec, plan) yazılması teyit edilmedi.
- [ ] Companion implement stock `tasks.md` ile: task ID'leri tanınıyor
      (0.21.0 `task_sync.py:38`, `**` isteğe bağlı); dalga (`⟶ Wait`) ve
      `Files:` satırları yok, paralelleştirme haritası eksik. İlk koşuda
      gözlenir. Companion implement spec'i kendisi `completed` yapıyor.
      `devenv` 0.21.0'ı kuruyor; wiki notları main'e (9fd7ebae, 136 commit
      ileride) göre: 0.21.0 implement task'ları varsayılan olarak kendisi
      yazıyor ve capability kaydetmiyor.
- [ ] Anayasa şablonu 8 ilke ve 5 bölüm, 205 satır; wiki bulgusu 6-10
      yanlışlanabilir ilke. Constitution Check her ilke için satır yazıyor.
- [ ] ctrl'in bağlamı dolunca bir devir notu gerekli mi: emin değiliz; not
      context'i zehirleyebilir. ctrl'in kalıcı hâli bugün `record.md`,
      `roadmap.md`, `inputs/`.
- [ ] Rol metinlerindeki çıkarımlar, kullanıcı onayladı ama canlıda
      denenmedi: belirsizlikte ctrl'in clarify koşturması; plan kontrolünün
      üç sorusu (dayanak kanıt mı, anayasa/spec çelişkisi, aynı turdaki kararı
      boşa çıkarma); tasks kontrolü; ctrl.md'deki sürüm kartı.
- [x] VS Code eklentisi `companion-standard` preset'ini sormadan kuruyor mu:
      kuruyor, ama zip kurulumda komut düşüyor (devenv bölümündeki madde).

### Uygulama (2026-09-15)

- [x] `bin/devenv`: Companion 0.21.0 release zip'ten kuruluyor
      (`specify init --extension … --trust-extension-urls`), kurulamazsa
      durur; `node_replacement()` ve `templates/speckit/nodes/` kalktı;
      Companion workflow'unun `workflow add`'i kalktı; `living-specs.yml`
      `enabled: false` ile yaratılıyor. `5b60249`
- [x] `claude/skills/spike/SKILL.md`: fork içinde ajan açma yasağı. `355e6bb`
- [x] Çelişen eski maddeler ve "Rol metinleri" bölümü düştü. `f721362`
- [x] `claude/roles/{protocol,ctrl,impl}.md` baştan yazıldı; açıklar metinde
      `AÇIK`. README ve devenv `CLAUDE.md` akışa göre. `a7d12a1`
- [x] `templates/project/`: ctrl'e `roadmap.md`; `record.md` Kararlar,
      İtirazlar, Açık; impl'e ctrl'in roadmap'ini ve `inputs/`'unu okuma
      yasağı; testler 35/35. `b6c3cba`
- [x] Ürün soruları ctrl'de, roadmap'te referans ürün; research denemesi ve
      impl.md'deki ajan satırı çıktı; impl'in `handoff.md`'si şablondan,
      exclude'dan ve rol metninden kalktı. protocol.md ve impl.md yalnız
      yönlendirmeye indi, gerisi ctrl.md'ye taşındı. impl'in ctrl'e erişimi
      kalktı: `additionalDirectories` yok, `Read` ctrl'in bütün dizinine
      yasak, `record.md` gösterilmiyor. `da39d57`, `0a1b7fd`
- [x] Global `CLAUDE.md`'nin wiki kuralından proje adı çıktı: "dağıtılan araç
      (kendi reposunun işi)". `16b319b`
- [ ] Gerçek `./install.sh` koşulmadı: kurulu `~/.config/claude/roles` ve
      `~/.config/claude/CLAUDE.md` hâlâ eski metin.

## Tasarım (konuşuldu, uygulanmadı)

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
- [ ] Companion sürümü artarken zip'te `presets/` var mı bakılır. VS Code
      eklentisi (0.32.0) proje açılınca ve Companion dizini değişince,
      `.specify/presets/companion-standard` yoksa sormadan
      `specify preset add --dev .specify/extensions/companion/presets/companion-standard`
      koşuyor; preset 7 stock `speckit-*` skill'ini değiştirir. 0.21.0 zip'inde
      `presets/` yok, komut düşüyor ve yalnız log'a yazılıyor; stock kalıyor.
- [ ] dbaas'ta 7 stock skill `preset:companion-standard`'dan geliyor
      (Companion klondan kurulmuştu, VS Code preset'i kurdu); yeni rol metni
      stock varsayıyor. Muhtemel düzeltme, denenmedi: Companion'ı zip'ten
      `--force` ile yeniden kur, sonra `specify preset remove companion-standard`;
      sıra ters olursa VS Code preset'i geri kurar.
- [ ] Repo adı `devenv`, iç adlar hâlâ `dev-templates`: yerel dizin,
      `~/.local/share/dev-templates`, `DEV_TEMPLATES_REF`, flake input adı.
- [ ] README'deki "Claude Code skill" bölümü `skills/devenv`'i anlatıyor; repoda
      böyle bir dizin yok.
- [ ] `SPECKIT_INTEGRATION_CLAUDE_EXTRA_ARGS` kuruluma girmiyor; koşuyu başlatma
      biçimi README'de durmalı.
- [ ] `~/workspace/ai-rules/rust.md` kuralın ikinci kopyası; tek kaynak
      `templates/rules/`.
- [ ] `devenv` kurduğunu geri alamıyor. Spec Kit'in yönetim alanı dışında
      kurdukları: kökteki `living-specs.yml`, `extensions.yml`'de kapatılan
      git commit hook'ları. `specify extension remove` bunları bilmez. dbaas'ta
      orkestrasyon 2026-09-14'te söküldü: extension ve workflow `specify` ile,
      hakem, `Stop` hook'u, `implement-exec` ve spike kopyası elle, ardından
      `build-pipeline.py`. `devenv update` ile birlikte düşünülmeli.
- [ ] Kurulu kopya kaynaktan ayrışınca bunu gören bir kontrol yok: config'teki
      `roles/` ve `skills/`. `devenv --version` yalnız
      kurulu `bin/devenv`'in commit'ini söylüyor.
- [ ] Branch adını Spec Kit'in git extension'ı, spec dizininin adını Companion
      ayrı ayrı türetiyor. Bir specify koşusunda aynı çıkıyor mu bilinmiyor.
      Çıkmazsa bir şey kırılmaz (Spec Kit dizini `feature.json`'dan buluyor),
      yalnız branch ile dizin eşleşmez.
