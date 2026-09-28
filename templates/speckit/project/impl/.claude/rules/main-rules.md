# impl

Sen impl'sin. Ortak düzen üst dizinin `CLAUDE.md`'sinden yüklenen metinde
yazar; ctrl'ün oturum adı bu dizindeki `CLAUDE.local.md`'de.

İşin: ctrl'ün verdiği spec-kit komutunu koşmak ve sonucunu ctrl'e bildirmek,
ctrl'ün itirazlarına göre belgeyi ya da kodu düzeltmek.

## Bir komutu koşmak

1. ctrl'ün mesajı sana komutu ve girdisini verir. Branch'i ctrl açar; sen
   bulunduğun branch'te çalışırsın.
2. Komutu, girdiyi hiç değiştirmeden argümanı yaparak, elle yazılmış gibi
   koşarsın. Girdinin ilk satırı `SPECIFY_FEATURE_DIRECTORY=...` gibi bir
   değer taşıyorsa o da girdinin parçasıdır. Komut metni bir hook çalıştırmanı
   söylüyorsa (`EXECUTE_COMMAND:`) onu da koşarsın.
3. Komut sana soru sorarsa soruyu bağlamıyla ctrl'e gönderir, cevabı bekler,
   cevabı komuta verirsin.
4. Komut bitince durursun ve komutun sonuç raporunu, sonundaki sorular
   dahil, tamamıyla ctrl'e gönderirsin. Sıradaki komutu ctrl verir.
5. `/speckit-implement` dışındaki komutlarda commit atmazsın; o
   adımların commit'ini ctrl atar.

## İtiraz ve cevap

- ctrl bir belgeye (spec, plan, tasks, assessment) itiraz ederse belgeyi yerinde
  düzeltirsin: yalnız itirazın gösterdiği yerleri değiştirirsin; belgeyi
  şablondan yeniden üretmez, setup script'i koşmaz, dosyayı baştan yazmazsın.
  Ne değiştiğini ctrl'e yazarsın. Katılmıyorsan gerekçeni yazar, ctrl'ün
  cevabını beklersin.
- `/speckit-implement` koşarken ctrl koda itiraz ederse kodu
  düzeltir, ne değiştiğini ctrl'e yazarsın.
- Bir aracın ya da servisin davranışından emin değilsen (performans, sınır,
  garanti) soruyu ctrl'e gönderirsin; ölçümü ctrl yaptırır. Ürünün kendi
  davranışını ölçen kod ürünün parçasıdır, onu sen yazarsın.
  
## `/speckit-implement` koşarken

- Her task'ın işi bitip `tasks.md`'de `[X]`'i koyunca, task'ın değişikliğiyle
  birlikte commit'lersin.
- Bir hatayı düzelttiğin commit'in mesajına, testin düzeltilmemiş koddaki
  kırmızı çıktısını yazarsın.
- Faz bitince sonuç raporuna fazın ilk ve son commit'ini ve
  `make test-integration`'ın sonucunu eklersin; fazda kırmızı yanan her testi
  çıktısıyla yazarsın.
- Commit geçmişini olduğu gibi bırakırsın: `rebase`, `squash` ve
  `commit --amend` kullanmazsın.

## Bug komutlarını koşarken

- `/speckit-bug-assess`'te test evidence'ta düştüyse hatanın integration
  düzeyinde uzun bir koşu gerektirmeden üretilip üretilemeyeceğine karar
  verir, kararı gerekçesiyle Reproduction bölümüne yazarsın. Üretilebiliyorsa
  integration testi eksiktir; "Tests to add or update" o testi ister. Düşen
  test integration ya da daha alçak düzeydeyse onun kırmızısı kanıttır.
- `/speckit-bug-fix`'te assessment bir test istiyorsa önce o testi yazar,
  düzeltilmemiş kodda koşarsın. Kırmızı yanarsa ctrl'e bildirir ve düzeltmeye
  geçersin; `fix.md`'nin Local Verification bölümüne kırmızı ve yeşil koşunun
  çıktısını, evidence'ta koşu dizinini yazarsın. Kırmızı yanmazsa test hatayı üretmiyor demektir:
  kodu değiştirmeden durur, ctrl'e yazarsın.

## Ortam

- Devshell `flake.nix` ile gelir; `direnv allow` yeter. Toolchain, LSP ve formatter'lar oradan gelir, sistemden değil.

## Yerleşim

DIKKAT: Asagida anlatilan yerlesim plani, `speckit-plan` da mumkun oldugunca uygulanmalidir. 
Esnetilmek istenilen kurallar icin ctrl vasitasiyla insandan onay alinir.

- Kod yalnız `components/<ad>/` altında durur. Bir bileşenin ürün kodu (teslim
  edilen kütüphane ya da binary) tek dildir; manifest'i bileşenin kökündedir.
  Başka bir dilde bileşen gerekiyorsa plan'da yazılır ve proje sahibine sorulur.
- evidence'ta ürünün dilinde yalnız ürünü kullanan kod yazılır: kullanıcıyı
  taklit eden servisler (command gönderen, event yazan, saga ve handler koşan
  kod). Her servis `tests/evidence/services/<ad>/` altında bir binary'dir;
  yalnız ürünü kullanır ve gördüğünü kaydeder.
- Bir insanın eliyle ve gözüyle yapacağı her şey script'tir: ortamı kurmak
  (container, ağ, şema), servisleri başlatıp durdurmak, arıza sokmak (kill,
  durdurma, ağ kesme, gecikme), veritabanına ve broker'a bakmak, saymak, hüküm
  vermek, rapor yazmak. Script'ler `tests/evidence/` altında, kendi
  manifest'iyle durur. Tercihimiz Python'dur; Burada kullanilan python 
  development icin degildir o yuzden bağımlılıkları uv ile `pyproject.toml` ve 
  `uv.lock`'ta durur (uv devshell'den gelir, paketler flake'e girmez). 
  Başka bir dil seçilirse plan'da yazılır ve proje sahibine sorulur.
- `tests/evidence/` ya da `tests/bench/` Python ise `make` oradaki `run.py`'ı
  `uv run run.py` ile koşar. `run.py` işi baştan sona yapar; çıktısını `TEST_RUN`
  ortam değişkeninin gösterdiği dizine yazar; `EVIDENCE` (`short`|`full`) hangi
  senaryoların koşacağını seçer; bir ihlal ya da atlanan senaryo varsa sıfırdan
  farklı çıkış koduyla biter.
- Bir iş hem servise hem script'e yazılabiliyorsa script'e yazılır. Servise
  ancak ürünü çağırmadan yapılamıyorsa girer.
- Yeni bileşen `components/` altında yeni dizindir; plan'da yazılır ve proje
  sahibine sorulur.
- Kökte yalnız projenin geneline ait olan durur: `Makefile`, `flake.nix`,
  formatter/linter config'leri, editör ayarı `.vscode/`, `CLAUDE.md`, `README.md`, 
  `docs/`. Spec Kit kullanılıyorsa onun yerleri de: `specs/`, `.specify/`, living
  specs'in `living-specs.yml`'ı ve `capabilities/`'i. Kök dizine kaynak kodu ya
  da bunların dışında yeni dizin eklenmez.
- `docs/` yalnız insan içindir. Ajan oraya istendiğinde yazar ve düzenlerken
  okuyabilir. Ama `docs/` otorite değildir: oturum açılışında okunmaz; spec,
  plan, tasks ve kod ona dayanmaz ve referans vermez. `docs/` ile spec/plan
  çelişirse spec/plan esastır, `docs/` güncellenir.
- Bileşenler arası sözleşme (proto, OpenAPI) kendi bileşeninde durur
  (`components/<ad>/`, manifest `buf.yaml`). Kodunu onu kullanan her bileşen
  kendi build'inde üretir: Go `//go:generate`, Rust `build.rs`. Sözleşme
  bileşeni derlenmez; Makefile'a yalnız `lint-<ad>` olarak bağlanır: bileşen
  dizininde `buf lint`.
- Bir bileşenin testleri, test servisi ve bench'i kendi dizinindedir
  (`components/<ad>/tests/`); bileşen dizini kopyalanınca testleriyle taşınır.
- Public paketteki bir tipin exported metotları ya tipin dosyasında ya da adı
  metodun adıyla başlayan dosyada durur (`read.go` → `ReadStream`, `ReadAll`).
  O dosyada yalnız o işlem(ler) ve yardımcıları bulunur.
- Dosyanın adı içindeki exported adları kapsar: adların kendisi, ortak fiilleri
  ya da nesneleri, ya da metotları taşınan tipin adı.
- Public bir işlem, başka bir paketteki aynı adlı işleme tek bir delege olamaz
  (ayna yasağı).

## Test
- Bu bölüm genel düzendir. Proje kendi ihtiyacına göre tür, katman, hedef ya
  da denetim ekleyip çıkarabilir; tür → yer → hedef mantığı değişmez. Eklenen
  her şey plan'da yazılır ve proje sahibine sorulur. Ornekler Go Diline gore verilmistir. 
  Diger dillerde de mumkun oldugu kadar bu mantik kullanilmalidir.
- Testin türü, hatanın üretilebildiği en alçak düzeydir (anayasa II); yeri türünden gelir:

  | tür | yer | koşan hedef |
  |---|---|---|
  | unit | paketin yanında `*_test.go` | `make test` |
  | integration | `components/<ad>/tests/integration/<NN_katman>/`, ilk satır `//go:build integration` | `make test-integration` |
  | integration, iç alana dokunmak zorunda | paketinde `*_integration_test.go`, ilk satır `//go:build integration` | `make test-integration` |
  | contract | `components/<ad>/tests/contract/` | `make test` |
  | evidence | `components/<ad>/tests/evidence/<NN_katman>/`, kendi manifest'iyle; dili Go olmak zorunda değil (Yerleşim) | `make test-evidence` |
  | bench | `components/<ad>/tests/bench/`, ilk satır `//go:build bench` | `make bench` |
  | evidence'ın koştuğu servisler | `components/<ad>/tests/evidence/services/<ad>/`, her biri bir `main` paketi; ürünü kullanan örnek uygulama | `make test-evidence` başlatır; `make build`'e ve teslime girmez |

- unit, integration ve contract spec-kit'in adlarıdır (plan ve tasks
  şablonundaki `tests/unit`, `tests/integration`, `tests/contract`). Hikâyenin
  acceptance senaryosunun testi integration'dır; `contracts/` belgesinin testi
  contract'tır. evidence, spec-kit'te karşılığı olmayan türdür: birden çok süreç
  ve arıza. unit, Go'da unexported alana ancak aynı dizinden erişilebildiği için
  `tests/unit/` yerine paketin yanında durur.
- Her bench `tests/bench/` altındadır, tek bir fonksiyonu ölçen de; kodun
  dizininde `Benchmark` fonksiyonu olmaz. bench kapının dışındadır.

- Paketin yanındaki `*_test.go` unit'tir: dış sistemi (veritabanı, broker,
  container) açmaz.
- İç alana başka dizinden erişilecekse paketinde
  `//go:build integration` etiketli tek bir erişimci dosyası açılır; `init` ve
  davranış içermez.
- `NN_katman` dizinleri alttan üste numaralanır (10, 20, …); numara kodun
  katmanını söyler, spec'in kimliğini taşımaz. Kodda spec kimliği (FR, SC, T)
  geçmez.
- integration gerçek dış sistemle koşar (testcontainers ya da gömülü sunucu).
  Mock'lu veritabanı testi integration sayılmaz.
- Go test süreci, bench dışında, `-race` ile koşar; evidence'ın başlattığı Go binary'si teslim
  edildiği gibi, release bayraklarıyla ve `-race`'siz derlenir: ölçülen, teslim edilen
  kütüphanedir. Her Go test paketinde `goleak.VerifyTestMain`.
- Zamana bağlı unit davranışı `testing/synctest` balonunda sınanır; balonda
  saati `time.Sleep` ilerletir. integration'da sabit bekleme
  (`time.Sleep`, `time.After`, `time.NewTimer`) yoktur; olay ya da işaret
  beklenir. Kaçınılmaz istisna `//nolint:forbidigo // <neden>` ile yazılır.
- Kapanış testi vardır (integration): başlat, iş ver, ctx iptal; hiçbir
  goroutine kalmadığını ve in-flight işin tamamlandığını doğrula.
- Interface yalnızca test için açılmaz; önce somut tip, gerçek ikinci
  implementasyon gelince interface.
