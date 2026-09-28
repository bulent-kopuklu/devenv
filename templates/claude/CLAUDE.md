# PROJECT_NAME

<!-- Tek paragraf: bu proje ne yapar, kim için. -->

## Ortam

- Devshell `flake.nix` ile gelir; `direnv allow` yeter. Toolchain, LSP ve formatter'lar oradan gelir, sistemden değil.
- Build / test / lint kökteki `Makefile`'dan: `make`, `make test`, `make lint`,
  `make dist`, `make clean`, `make distclean`. Parametreler (`VARIANT`, `TARGET`,
  `COMPONENTS`) ve varsayılanları dosyanın başında.
- Test hedefleri türe göredir: `make test` (unit ve contract), `make test-integration`,
  `make test-evidence`, `make bench` (kapının dışında). Türlerin yeri dilin kural
  dosyasının "Test" bölümünde.
- `make gate` sırayla `build`, `lint`, `test`, `test-integration`
  ve `test-evidence` koşar. Bir türün testi yoksa hedefi boş geçer. Her koşunun
  çıktısı `RUNS` altına koşu başına bir dizine yazılır; `clean` ve `distclean`
  ona dokunmaz, yalnız insan temizler.

## Yerleşim

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
  manifest'iyle durur. Tercihimiz Python'dur; bağımlılıkları uv ile
  `pyproject.toml` ve `uv.lock`'ta durur (uv devshell'den gelir, paketler
  flake'e girmez). Başka bir dil seçilirse plan'da yazılır ve proje sahibine
  sorulur.
- `tests/evidence/` ya da `tests/bench/` Python ise `make` oradaki `run.py`'ı
  `uv run run.py` ile koşar. `run.py` işi baştan sona yapar; çıktısını `TEST_RUN`
  ortam değişkeninin gösterdiği dizine yazar; `EVIDENCE` (`short`|`full`) hangi
  senaryoların koşacağını seçer; bir ihlal ya da atlanan senaryo varsa sıfırdan
  farklı çıkış koduyla biter.
- Bir iş hem servise hem script'e yazılabiliyorsa script'e yazılır. Servise
  ancak ürünü çağırmadan yapılamıyorsa girer.
- Yeni bileşen `components/` altında yeni dizindir; plan'da yazılır ve proje
  sahibine sorulur. Açıldığı commit'te kökteki `Makefile`'a bağlanır:
  `<hedef>-<ad>` reçeteleri yazılır, toplu hedefler onları çağırır. Dilin
  reçeteleri `.claude/rules/<dil>.md`'nin Makefile bölümünde. `Makefile`'ın
  başındaki arayüzde olmayan bir hedef ya da parametre gerekiyorsa plan'da
  yazılır ve proje sahibine sorulur.
- Kökte yalnız projenin geneline ait olan durur: `Makefile`, `flake.nix`,
  formatter/linter config'leri, editör ayarı `.vscode/`, `CLAUDE.md`, `README.md`, `docs/`. Spec Kit kullanılıyorsa onun yerleri de: `specs/`, `.specify/`, living
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
- Build çıktısı `build/<target>/<variant>/`, release çıktısı `dist/<target>/`.
- Bir bileşenin testleri, test servisi ve bench'i kendi dizinindedir
  (`components/<ad>/tests/`); bileşen dizini kopyalanınca testleriyle taşınır.
- Public paketteki bir tipin exported metotları ya tipin dosyasında ya da adı
  metodun adıyla başlayan dosyada durur (`read.go` → `ReadStream`, `ReadAll`).
  O dosyada yalnız o işlem(ler) ve yardımcıları bulunur.
- Dosyanın adı içindeki exported adları kapsar: adların kendisi, ortak fiilleri
  ya da nesneleri, ya da metotları taşınan tipin adı.
- Public bir işlem, başka bir paketteki aynı adlı işleme tek bir delege olamaz
  (ayna yasağı).

<!-- Bileşenler ve rolleri. -->

## Kurallar

- Global `CLAUDE.md`'deki kurallar burada da geçerli; bu dosya yalnızca projeye özel olanları taşır.


<!-- SPECKIT START -->
<!-- SPECKIT END -->

<!-- /init çıktısını bu satırın altına ekle; yukarıdaki bölümleri koru. -->
