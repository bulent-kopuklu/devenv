# Go'da test

`testing.md`'nin Go karşılıkları.

## Unit

- Go'da unexported adlara yalnız aynı paket erişir; `tests/unit` diye bir
  yer olamaz. Unit test paketin yanında `*_test.go`'dur.
- Dosya, sınadığı kodun adını alır: `acquire.go` → `acquire_test.go`.
- Etiketsizdir (`//go:build` yok).

## `tests/` modülü

- `tests/` iç içe ikinci modüldür: `module <modül>/tests`; ürünü `require`
  eder ve `replace <modül> => ../` ile kullanır. Bu `replace` kalıcıdır.
  `go mod tidy` bu modülde de temiz kalır.
- Bileşen kökündeki `./...` `tests/`'e inmez: testler ürünle derlenmez,
  teslime ve yayımlanan modüle girmez.

## `-race`

- Testler `-race` ile koşar; alt process'ler de `-race`'lidir. `-race` cgo
  ister: binary `CGO_ENABLED=0` ile derlense de testler cgo'lu derlenir.

## Acceptance

- `tests/acceptance/` tek bir pakettir; dosyalar `s001-sc-002-<ad>_test.go`,
  `s001-us-006-<ad>_test.go`.
- `internal` paketlerinin exported adları kullanılabilir: Go'nun `internal`
  kuralı path'e bakar, modül sınırına değil; `…/<ad>/tests`,
  `…/<ad>/internal/*`'ı import edebilir (deneyle doğrulandı). Unexported'a
  erişim ve ürüne test hook'u yok.
- Ürünün birden çok instance'ını isteyen testte her instance test
  binary'sinin bir alt process'idir: test binary'si kendini rolü taşıyan bir
  ortam değişkeniyle yeniden başlatır, `TestMain` değişkeni görünce rolü
  koşar.
- Uzun ölçüm `-short`'la ayrılır: `testing.Short()` ise atlanır.

## Sistem senaryosu

- `tests/scenario/` tek bir pakettir; dosyalar `s001-ss-001-<ad>_test.go`.
- Acceptance'ın Go maddelerinin hepsi geçerlidir: `internal` paketlerinin
  exported adları, alt process instance'lar, `-short`.
- `tests/internal/*`'ı kullanır: bir `internal` dizinini üst dizininin
  altındaki her paket import edebilir; `tests/internal`'ın üstü `tests/`'tir.

## Yardımcılar

| kim kullanıyor | yer | örnek |
|---|---|---|
| ürün paketlerinin testleri de | ürün modülünde `internal/testutils/` ve alt dizinleri | `testutils`, `pgtest`, `twin`, `netfault` |
| tek bir paketin sahtesi | paketin yanında `<paket>test` | `internal/lease/leasetest` |
| yalnız acceptance ve sistem senaryoları | `tests/internal/<iş>/` | `system`, `modules`, `teststore`, `ticks`, `checkout`, `sensors`, `wait`, `latewrite` |

- Ürün modülü `tests` modülünü import edemez (modüller arası döngü); paket
  testlerinin kullandığı yardımcı bu yüzden ürün modülünde, `internal/`
  altında durur.
- `tests/internal/*`'ı yalnız `tests` modülü import eder: ürüne derlenmez,
  kütüphaneyi kullananlara açılmaz.
- Bir yardımcının ikinci bir kullanıcısı çıkarsa yukarı taşınır (`netfault`,
  `pgstore`'un unit testi de kullanınca `tests/internal`'dan
  `internal/testutils`'e geçti).
- Her test paketinin girişi aynı tek satırdır:
  `func TestMain(m *testing.M) { testutils.Main(m) }`. Paketin container'ını
  kapatır, goroutine sızıntısını (`goleak`) denetler, alt process rolünü
  koşar, coverage açıksa alt process'in coverage'ını yazar.

## Fixture'lar

- `tests/fixtures/<konu>/<sürüm>/` (bugün `tests/fixtures/wire/1/`); contract
  testi oradan okur.

## `go.md`'nin test koduna uygulanmayan bölümleri

- "Fonksiyon boyu ve yapı" ile "Panic ve recover" `_test.go` dosyalarına
  uygulanmaz.

## Elenen yollar

- `export_test.go`: başka bir paketten ya da modülden görünmüyor (deneyle
  doğrulandı).
- CockroachDB `TestingKnobs`, HashiCorp `testing.go`, nats ve etcd'nin "yalnız
  testte kullan" fonksiyonları: public API'ye sızıyor; knob'lar ürün kodunda
  runtime dalı açıyor.
- Build tag'li hook dosyası (`//go:build testonly`): yalnız Vault'ta, birkaç
  özellik için; ana yol olarak kullanan yok.
- grpc modelindeki hook'lar: ancak black-box'a çevrilemeyen bir test çıkarsa
  düşünülecekti; hiç gerekmedi.
