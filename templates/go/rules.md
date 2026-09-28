# Go Kuralları

Go kodu yazarken uyulan standart; kütüphane ve servis için.

## Dosya ve yardımcılar
- Dosyada önce dışarı verilenler durur (public tipler, public fonksiyonlar ve
  metotlar), altında unexported yardımcılar. Hiçbir unexported fonksiyon bir
  public bildirimin üstünde durmaz.
- Bir unexported yardımcıyı başka bir dosya da kullanmaya başlarsa yardımcı
  artık o işlemin değildir; aynı commit'te dosyasından çıkar: bir tipin
  metoduysa tipin kendi dosyasına, değilse ne iş yaptığını söyleyen bir dosyaya
  (`codec.go`), birden çok paket kullanıyorsa bir `internal/` paketine. Testlerin
  çağırması bu kurala girmez.

## Yerleşim
- Bileşen bir Go modülüdür; `go.mod` bileşen kökündedir
  (`components/<ad>/go.mod`). Modül yolu repo'nun yolu ve bileşenin
  dizinidir (`<repo>/components/<ad>`): `go get` modülü bu yoldan bulur.
  Go'da `src` yoktur; kaynak modül kökündedir.
- Modül düzeni Go'nun belgesine uyar (https://go.dev/doc/modules/layout):
  public paket kökte, destek paketleri `internal/<ad>/` altında, teslim edilen
  binary'ler `cmd/<ad>/` altında. Paket olabildiğince `internal/`'dadır.
- Kod, tiplerinin paketinden aşağı inmez: bir internal paket üst paketin
  tiplerine `reflect.Value`, `any` ya da geri çağrı üzerinden ulaşmak zorunda
  kalıyorsa o kod üst pakette kalır.
- `tests/` iç içe ikinci modüldür: `module <modül>/tests`; ürünü `require`
  eder ve `replace <modül> => ../` ile kullanır. Yolu ürünün yolunun altında
  olduğu için ürünün `internal` paketlerini import edebilir, unexported adlara
  erişemez. Testlerin ortak yardımcısı (ör. `internal/testenv`) ürünün
  `internal/`'ında tek kopya durur. İç içe modül bileşen kökündeki `./...`'e
  ve yayımlanan modüle girmez; `tests/` teslimden böyle ayrılır.
- Kardeş bileşeni kullanan bileşen onu `require` eder ve
  `replace <kardeş> => ../<kardeş>` ile monorepo'daki kopyasını kullanır.
  `replace` yalnız ana modülde geçerlidir: bileşeni `go get` ile çeken,
  kardeşini `require`'daki sürümden alır. Yayımlanan bileşen
  `components/<ad>/vX.Y.Z` tag'iyle sürümlenir.
- Public paketteki bir tipin exported metotları ya tipin dosyasında ya da adı
  metodun adıyla başlayan dosyada durur (`read.go` → `ReadStream`, `ReadAll`).
  O dosyada yalnız o işlem(ler) ve yardımcıları bulunur.
- Dosyanın adı içindeki exported adları kapsar: adların kendisi, ortak fiilleri
  ya da nesneleri, ya da metotları taşınan tipin adı.
- Public bir işlem, başka bir paketteki aynı adlı işleme tek bir delege olamaz
  (ayna yasağı).

## Kütüphane
- Logger, metrik ve trace sağlayıcısını kullanan uygulama verir: `*slog.Logger`,
  OpenTelemetry `MeterProvider` ve `TracerProvider`, config'in seçenekleri
  olarak. Verilmezse `slog.Default()` ve OpenTelemetry'nin global sağlayıcıları
  kullanılır. Kütüphane handler, exporter ya da log seviyesi seçmez.
- Kütüphane kendi döngülerinin sınırında loglar (worker döngüsü, sunucunun
  cevap veremediği istek); alt katmanlar hatayı sarıp döner, loglamaz.
- Kütüphane env okumaz; ayarlarını config'le alır.

## Servis
- `main` tek iş yapar: `os.Exit(run())`. `run(ctx) error` içinde config, wiring,
  sinyal, serve. `log.Fatal`/`os.Exit` başka yerde yok; defer'lar çalışmaz,
  bağlantılar yarım kalır.
- Config tek kaynaktan (env ya da dosya) `run` başında bir struct'a parse edilir
  ve doğrulanır; doğrulanamayan config'le süreç başlamaz. Kod içinden
  `os.Getenv` çağrısı yok. Sır (parola, token) loglanmaz; config struct'ın
  `LogValue()`'su maskeler.
- Tek logger `run`'da kurulur ve bağımlılık olarak geçilir. `fmt.Println` ve
  `log.Printf` üretim kodunda yok.
- Sinyal: `signal.NotifyContext(ctx, SIGTERM, SIGINT)`. Kapanış sırası kodda tek
  bir yerde, okunur şekilde durur: yeni iş almayı durdur, in-flight işi süreli
  bekle, bağımlılıkları kapat, çık.

## Goroutine
Her goroutine'in sahibi, bitiş koşulu ve hata yolu vardır.
- Çıplak `go f()` yok. Ömür `errgroup.Group` (hata toplama + ctx iptali) veya
  `sync.WaitGroup` ile bağlanır; `Wait` eden biri vardır.
- Goroutine ctx alır ve `ctx.Done()`'ı dinler. ctx'siz sonsuz döngü yazılmaz.
- Worker sayısı sınırlı ve config'ten gelir. "Mesaj başına goroutine" yok;
  semaphore veya sabit worker havuzu.
- Kanal boyutu bilinçli ve sınırlı. Unbounded kuyruk (slice'a kontrolsüz append,
  arka arkaya `go` ile üretilen iş) yok; backpressure üst katmana iletilir,
  bellekte biriktirilmez.
- Kanalı yalnızca üretici kapatır, tek üretici; çoklu üreticide `WaitGroup` + tek
  kapatıcı. Tüketici kapatmaz.
- Mutex kritik bölgesinde I/O, kanal işlemi, callback yok. Kilit sırası sabit.

## Context
- Sınırdan giren her fonksiyon ctx alır, aşağı geçirir. `context.Background()`
  yalnızca main/test; `context.TODO()` commit edilmez.
- ctx struct'ta saklanmaz. Saklanırsa iptal semantiği kaybolur.
- Context'e yalnızca request-scoped meta (correlation id, principal). Logger, DB,
  config context'te taşınmaz.
- Her dış çağrının zaman sınırı vardır: `context.WithTimeout` veya client-level
  timeout. `http.DefaultClient` (timeout'suz) yasak.
- Çağrıdan bağımsız süren iş (döngü, zamanlayıcı) çağıranın ctx'ine bağlanmaz;
  kendi ömür ctx'i vardır. Aksi halde çağrı bitince iş yarım kalır.

## Fonksiyon boyu ve yapı
- Bir fonksiyon tek iş yapar; gövdesi ekrana sığar (~50 satır).
- Closure (func literal) birkaç satırlık yapıştırıcıdır. Birkaç satırı geçen,
  dallanan ya da hata üreten closure isimli fonksiyon ya da method olur.
  Closure'lardan oluşan struct (`StructName{Member1: func…, Member2: func…}`) yerine
  interface'i isimli bir tip uygular.
- switch/select'in her case'i birkaç satırdır; iş, case'in çağırdığı
  fonksiyondadır.
- İç içe blok derinliği en çok 3.
- Bu bölüm `_test.go` dosyalarına uygulanmaz.
- `.golangci.yml`'deki `funlen` ve `gocognit` yalnız açık aşımı yakalar; norm bu
  bölümdür. Aşan fonksiyon bölünür, `//nolint` yazılmaz.

## Hata
- Hata değerdir; panic programcı hatasıdır. Ağ, I/O, parse, DB, bus → error.
- `if err != nil { return fmt.Errorf("<op>: %w", err) }`. Bağlam ekle, mesajı
  tekrarlama, çıplak `return err` yalnızca en alt katmanda.
- Sentinel (`var ErrNotFound = errors.New(...)`) ve hata tipleri;
  `errors.Is`/`errors.As`. Mesaj string'ine bakarak karar veren kod yok.
- Hata yutma yok: `_ = f()` gerekçe yorumuyla, boş `if err != nil {}` yok.
- Hata bir kez loglanır: sınırda (handler, worker döngüsü). Alt katman sarar ve
  döner, loglamaz.

## Kapalı tip kümesi
- Üyeleri belli bir tip kümesi (ör. mesaj ya da event türleri) interface ile
  ifade ediliyorsa interface'e `//sumtype:decl` yazılır ve en az bir unexported
  metodu olur. `gochecksumtype` o interface üzerindeki her type switch'te eksik
  case'i yakalar; `default` dalı eksik case'in yerini tutmaz.

## Panic ve recover
`recover` yalnızca kendi goroutine'indeki panic'i yakalar; `recover`'ı olmayan
bir goroutine'de çıkan panic bütün süreci düşürür.
- Her goroutine'in girişinde (`errgroup`'a verilen fonksiyonlar dahil) ve her
  istek ya da mesaj handler'ında `recover` vardır.
- Yakalanan panic: stack loglanır, panic `error`'a çevrilip goroutine'in
  sahibine döner. Goroutine kendini sessizce yeniden başlatıp devam etmez;
  hatayı sahibi görür ve karar verir.
- `recover` ile hata akışı kurulmaz: beklenen hata `error` döner.

## Dış bağımlılıklar
- Retry yalnızca idempotent işlemde; üst sınır (deneme sayısı VE toplam süre),
  exponential backoff, jitter. Retry her denemeyi değil sonucu loglar.
- Bağımlılık uzun süre düşükse hızlı-başarısızlık; her isteğin timeout'a kadar
  beklemesi goroutine ve bağlantı biriktirir.
- Bağlantı havuzları sınırlı ve config'ten.
- Süre ölçümü `time.Since` (monotonic). Zaman damgası UTC.

## Bağımlılık ve derleme
- `go.mod`/`go.sum` commit; ürünün ve `tests/`'in modülünde `go mod tidy`
  temiz; `replace` gerekçeli ve geçici; kardeş bileşene ve `tests/`'ten ürüne
  `replace` kalıcıdır (Yerleşim).
- Eklemeden önce stdlib ve `golang.org/x`'e bak; 20 satırlık işe kütüphane
  eklenmez.
- `go.mod`'a `toolchain` direktifi yazılmaz. Go sürümü devshell'den gelir;
  `GOTOOLCHAIN=auto` olduğu için devshell'dekinden yeni bir direktif go'ya başka
  bir toolchain indirtir.
- Binary `CGO_ENABLED=0` ile statik derlenir; cgo açılırsa gerekçe yazılır.
  Testler cgo'lu koşar: `-race` cgo ister.
- Binary'ye sürüm/commit `-ldflags "-X"` ile gömülür ve başlangıç log'unda
  görünür.

## Test
- unit paketin yanında `*_test.go`'dur; Go'da unexported ada yalnız aynı
  paketten erişildiği için `tests/unit/` yoktur.
- Exported API'yi kullanan integration `tests/integration/<NN_katman>/`'dadır
  ve etiket istemez. unexported'a dokunmak zorunda olan integration paketinde
  `*_integration_test.go`'dur, ilk satırı `//go:build integration`.
- Her test paketinde `goleak.VerifyTestMain`. `TestMain` etiketsiz bir
  dosyadadır; etiketli dosyada durursa etiketsiz koşuda derlenmez ve goleak o
  koşuda yoktur.
- Kodun paketinde `Benchmark` fonksiyonu olmaz; bench `tests/bench/`'tedir.
- Test süreci, bench dışında, `-race` ile koşar; evidence'ın başlattığı
  servisler `-race`'siz derlenir.
- Zamana bağlı unit davranışı `testing/synctest` balonunda sınanır; balonda
  saati `time.Sleep` ilerletir. integration'da `time.Sleep`, `time.After`,
  `time.NewTimer` yoktur. Kaçınılmaz istisna `//nolint:forbidigo // <neden>`
  ile yazılır.
- Interface yalnızca test için açılmaz; önce somut tip, gerçek ikinci
  implementasyon gelince interface.

## Makefile'da Go bileşeni
Bileşenin `Makefile`'ı `components/<ad>/`'da, `go.mod`'un yanındadır;
reçeteler orada, `tests/`'e ait olanlar `tests/` içinde koşar.
- `build`: önce `go generate ./...`, sonra
  `go build <bayraklar> ./...` ile bütün paketler; ardından main paketleri
  `go build <bayraklar> -o $(BIN)/ $$(go list -f '{{if eq .Name "main"}}{{.ImportPath}}{{end}}' ./...)`
  ile `$(BIN)`'e (liste boşsa bu adım atlanır). `go build -o <dizin>` main
  paketi olmayan modülde hata verdiği için bütün paketler ayrı derlenir.
  `./...` iç içe `tests/` modülüne inmez: testler ve evidence servisleri
  derlenmez, teslime girmez.
- Bayraklar: debug `-gcflags='all=-N -l'`, release `-trimpath -ldflags='-s -w'`.
- Her `go build` `CGO_ENABLED=0` ile koşar. Devshell `CC`'yi export ettiği için
  Go varsayılan olarak cgo'yu açar: host'ta binary nix'in glibc'sine dinamik
  bağlanır ve nix store'u olmayan makinede açılmaz, cross'ta host derleyicisi
  hedefi derleyemez. Testler `-race` için cgo'lu kalır. cgo isteyen bileşen ayrı
  karar ister; plan'da yazılır.
- `TARGET` host değilse `go build`'in önüne ayrıca `GOOS=linux` ve hedefin
  mimarisi gelir: aarch64 `GOARCH=arm64`, armv7 `GOARCH=arm GOARM=7`.
- `test`: `go test -race ./...`; contract testi varsa
  `tests/` içinde `go test -race ./contract/...`.
- `test-integration`: `go test -race -count=1 -tags integration ./...`
  (paketlerin yanındaki `*_integration_test.go` dosyaları); `tests/` içinde
  `go test -race -count=1 ./integration/...`.
- `test-evidence`: koşu dizini `$(TEST_RUN)/<ad>/test-evidence`'tır; `<ad>`
  bileşenin adıdır, `$(notdir $(CURDIR))`. `tests/` içinde servisler release
  bayraklarıyla, `-race`'siz
  `CGO_ENABLED=0 go build -trimpath -ldflags='-s -w' -o <koşu dizini>/bin/ ./evidence/services/...`
  ile koşu dizinine derlenir; sonra `tests/evidence/` içinde
  `TEST_RUN=<koşu dizini> uv run run.py`.
- `bench`: `tests/` içinde `go test -count=1 -timeout 60m -v -bench . ./bench/...`.
  Test ve Benchmark fonksiyonları birlikte koşar: container'lı ölçüm ve
  negatif kontrolleri Test fonksiyonu olarak da yazılabilir. go test'in
  varsayılan 10 dakikalık sınırı uzun bench'i panic'le keser; `-v` Test
  fonksiyonunun `t.Logf` ile bastığı sonucu gösterir.
- `lint`: bileşen kökünde ve `tests/` içinde `golangci-lint run ./...`;
  paketin yanındaki integration dosyalarını `.golangci.yml`'deki `build-tags`
  görünür kılar.
- `distclean`: boş.
