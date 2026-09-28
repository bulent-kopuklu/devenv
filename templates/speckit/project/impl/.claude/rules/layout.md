# Yerleşim ve test

DIKKAT: Asagida anlatilan yerlesim plani, `speckit-plan` da mumkun oldugunca uygulanmalidir. 
Esnetilmek istenilen kurallar icin ctrl vasitasiyla insandan onay alinir.

Bu dosya dilden bağımsızdır. Bir dilin kaynağı ve testleri nereye koyduğu,
`tests/`'i teslimden nasıl ayırdığı ve probe'larını nasıl derlediği
`.claude/rules/<dil>.md`'nin Yerleşim, Test ve Makefile bölümlerindedir.

## Yerleşim

- Ürün kodu yalnız `components/<ad>/` altında, ürünü dışarıdan ölçen kod
  yalnız `evidence/` altında durur. Bir bileşenin ürün kodu (teslim
  edilen kütüphane ya da binary) tek dildir. Başka bir dilde bileşen
  gerekiyorsa plan'da yazılır ve proje sahibine sorulur.
- Bileşen dizini bileşenin köküdür: kendi `Makefile`'ı, manifest'i (`go.mod`,
  `Cargo.toml` gibi), kaynağı ve `tests/`'i orada durur. Kaynağın yeri dilin
  alışkanlığıdır; dilin kural dosyası yazar.
- `tests/` bileşenin içindedir ama teslimin parçası değildir: derlenen,
  dağıtılan ya da yayımlanan pakete girmez.
- evidence ürünü dışarıdan, bir kullanıcı gibi ölçer: birden çok süreç, ağ ve
  arıza. Bileşenin değil sistemin testidir; kökteki `evidence/`'dadır:

  ```
  evidence/
  ├── Makefile                 devenv'den gelir
  ├── pyproject.toml, uv.lock  script'lerin manifest'i
  ├── sysenv/                  ortam düzeneği
  ├── <bileşen>/               yalnız bu bileşeni kullanan senaryolar
  │   ├── Makefile
  │   ├── probes/<ad>/         probe'lar
  │   ├── <NN_katman>/         senaryolar
  │   ├── setup/               bu bileşene özgü kurulum (şema, seed)
  │   └── check/               denetçiler
  └── systems/<ad>/            birden çok bileşeni kullanan senaryolar
      └── Makefile
  ```
- Probe ürünü bir kullanıcı gibi kullanan bir binary'dir (command gönderen,
  event yazan, saga ve handler koşan kod). Ürünün dilinde yazılır, yalnız
  ürünün public API'sini kullanır ve gördüğünü kaydeder. API'sini kullandığı
  bileşenin `probes/`'undadır; ortak kodu da orada, dilin kural dosyasının
  yazdığı yerdedir. Adı ürünün hangi kullanımını taklit ettiğini söyler
  (`saga-timeout`, `projection-local`); genel bir ad (`service`, `app`,
  `worker`) ya da senaryonun adını almaz. Bir probe'u birçok senaryo
  kullanabilir, bir probe tek bir senaryo için de yazılabilir.
- Probe ile parametre arasındaki sınır: gerçek bir kullanıcı farkı kodla
  yapıyorsa ayrı probe'dur; config'le ya da dağıtımla yapıyorsa (ürünün
  ayarları, yükün ölçeği, arızanın hedefi) parametredir. Sınama sorusu: değer
  değişince probe'un adı yalan olur mu?
- Tek bileşeni kullanan senaryo `evidence/<bileşen>/`'dedir; birden çoğunu
  kullanan `evidence/systems/<ad>/`'dedir. Sistem bir deployable bileşimidir;
  onu getiren plan adlandırır, sonraki plan'lar yoluyla anar. Sistem
  probe'ları kopyalamaz, bileşenin dizininden derletir. Yön tektir: sistem
  bileşenin evidence'ını kullanır; bileşen evidence'ı kullanmaz.
- Bileşenden bağımsız olan her şey `sysenv/`'dedir: container ve ağ kurmak,
  ağı yavaşlatmak, CPU ve belleği sınırlamak, microVM, arıza sokmak, çıktıyı
  yazmak. `sysenv/` hiçbir bileşenin adını ya da anlamını bilmez;
  `evidence/<bileşen>/setup/` yalnız o bileşene özgü kurulumu taşır.
- Bir insanın eliyle ve gözüyle yapacağı her şey script'tir: ortamı kurmak
  (container, ağ, şema), probe'ları başlatıp durdurmak, arıza sokmak (kill,
  durdurma, ağ kesme, gecikme), veritabanına ve broker'a bakmak, saymak, hüküm
  vermek, rapor yazmak. Script'ler `evidence/` altında, kendi
  manifest'iyle durur. Tercihimiz Python'dur; Burada kullanilan python 
  development icin degildir o yuzden bağımlılıkları uv ile `pyproject.toml` ve 
  `uv.lock`'ta durur (uv devshell'den gelir, paketler flake'e girmez). 
  Bir satırlık iş bash'le yazılır. Başka bir dil seçilirse plan'da yazılır
  ve proje sahibine sorulur.
- Her senaryo, adı neyi sınadığını söyleyen bir script'tir; adı spec'in
  kimliğini taşımaz.
- `make evidence:<ad>` dizinin giriş noktasını koşar: Python'da
  `uv run run.py`, yetiyorsa bir shell script'i. Giriş noktası işi baştan
  sona yapar; çıktısını `TEST_RUN` ortam değişkeninin gösterdiği
  dizine yazar; `SCENARIO` tek bir senaryoyu, `EVIDENCE` (`short`|`full`)
  hangi senaryoların koşacağını seçer; bir ihlal ya da atlanan senaryo varsa
  sıfırdan farklı çıkış koduyla biter.
- Bir iş hem probe'a hem script'e yazılabiliyorsa script'e yazılır. Probe'a
  ancak ürünü çağırmadan yapılamıyorsa girer.
- Yeni bileşen `components/` altında yeni dizindir; plan'da yazılır ve proje
  sahibine sorulur.
- Kökte yalnız projenin geneline ait olan durur: `Makefile`, `flake.nix`,
  formatter/linter config'leri, editör ayarı `.vscode/`, `CLAUDE.md`, `README.md`, 
  `docs/`, `components/`, `evidence/`. Spec Kit kullanılıyorsa onun yerleri de: `specs/`, `.specify/`, living
  specs'in `living-specs.yml`'ı ve `capabilities/`'i. Kök dizine kaynak kodu ya
  da bunların dışında yeni dizin eklenmez.
- `docs/` yalnız insan içindir. Ajan oraya istendiğinde yazar ve düzenlerken
  okuyabilir. Ama `docs/` otorite değildir: oturum açılışında okunmaz; spec,
  plan, tasks ve kod ona dayanmaz ve referans vermez. `docs/` ile spec/plan
  çelişirse spec/plan esastır, `docs/` güncellenir.
- Bileşenler arası sözleşme (proto, OpenAPI) kendi bileşeninde durur
  (`components/<ad>/`, manifest `buf.yaml`). Kodunu onu kullanan her bileşen
  kendi build'inde üretir: Go `//go:generate`, Rust `build.rs`. Sözleşme
  bileşeni derlenmez; Makefile'ında yalnız `lint` doludur: `buf lint`.
- Bir bileşenin unit, integration ve contract testleri ile bench'i kendi
  dizinindedir (`components/<ad>/tests/`); bileşen dizini kopyalanınca
  testleriyle taşınır. evidence bileşene değil sisteme aittir.

## Test

- Bu bölüm genel düzendir. Proje kendi ihtiyacına göre tür, katman, hedef ya
  da denetim ekleyip çıkarabilir; tür → yer → hedef mantığı değişmez. Eklenen
  her şey plan'da yazılır ve proje sahibine sorulur. Kodun yanında duran
  testlerin dosya adı, etiketi ve aracı dilin kural dosyasının Test
  bölümündedir.
- Testin türü, hatanın üretilebildiği en alçak düzeydir (anayasa II); yeri türünden gelir:

  | tür | yer | koşan hedef |
  |---|---|---|
  | unit | kodun yanında | `make test` |
  | integration | `components/<ad>/tests/integration/<NN_katman>/` | `make test-integration` |
  | integration, iç alana dokunmak zorunda | kodun yanında, integration diye ayrılmış | `make test-integration` |
  | contract | `components/<ad>/tests/contract/` | `make test` |
  | evidence | `evidence/<bileşen>/<NN_katman>/` ya da `evidence/systems/<ad>/`; script (Yerleşim) | `make evidence:<ad>` |
  | bench | `components/<ad>/tests/bench/` | `make bench` |
  | probe | `evidence/<bileşen>/probes/<ad>/`, her biri bir binary | `make build` derler, `make evidence:<ad>` derler ve başlatır; `$(BIN)`'e ve teslime girmez |

- unit, integration ve contract spec-kit'in adlarıdır (plan ve tasks
  şablonundaki `tests/unit`, `tests/integration`, `tests/contract`). Hikâyenin
  acceptance senaryosunun testi integration'dır; `contracts/` belgesinin testi
  contract'tır. evidence, spec-kit'te karşılığı olmayan türdür: birden çok süreç
  ve arıza. unit, iç alana eriştiği için `tests/unit/` yerine kodun yanında
  durur.
- Kodun yanındaki unit testi dış sistemi (veritabanı, broker, container)
  açmaz. Dış sistem açan test integration'dır; iç alana ve paketin test
  yardımcılarına dokunmuyorsa `tests/integration/`'dadır. Yardımcıya bağlı
  test onun yanında kalır; yardımcı iki yere kopyalanmaz.
- Her bench `tests/bench/` altındadır, tek bir fonksiyonu ölçen de; kodun
  yanında bench olmaz. bench ürünün uçtan uca özelliklerini süreç içinde kısa
  süre koşar ve sonucunu sürüm başına saklar; amacı sürümler arasındaki
  gerilemeyi görmektir. evidence'ın düzeneğini ve probe'larını kullanmaz.
  bench kapının dışındadır.
- `NN_katman` dizinleri alttan üste numaralanır (10, 20, …); numara kodun
  katmanını söyler, spec'in kimliğini taşımaz. Kodda spec kimliği (FR, SC, T)
  geçmez.
- integration gerçek dış sistemle koşar (testcontainers ya da gömülü sunucu).
  Mock'lu veritabanı testi integration sayılmaz.
- Probe teslim edildiği gibi, release bayraklarıyla derlenir: ölçülen,
  teslim edilen kütüphanedir.
- integration'da sabit bekleme yoktur; olay ya da işaret beklenir.
- Kapanış testi vardır (integration): başlat, iş ver, iptal et; arkada
  çalışan hiçbir iş kalmadığını ve in-flight işin tamamlandığını doğrula.
