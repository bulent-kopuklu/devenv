# Go Kuralları

Kapsam: uzun ömürlü, ağ üstünde konuşan, yeniden başlatılmadan haftalarca
çalışması beklenen Go servisleri. Kurallar üretimde servis düşüren hatalardan
türetilmiştir; her biri bir olayın karşılığıdır.

## Süreç ömrü
- `main` tek iş yapar: `os.Exit(run())`. `run(ctx) error` içinde config, wiring,
  sinyal, serve. `log.Fatal`/`os.Exit` başka yerde yok; defer'lar çalışmaz,
  bağlantılar yarım kalır.
- Başlangıçta doğrulanamayan config → hemen error, süreç başlamaz. Çalışırken
  keşfedilen config hatası en pahalı hata sınıfıdır.
- Sinyal: `signal.NotifyContext(ctx, SIGTERM, SIGINT)`. SIGTERM geldiğinde sırayla:
  1. readiness'ı kapat (yeni trafik gelmesin),
  2. listener'ları kapat (`http.Server.Shutdown`, gRPC `GracefulStop`, mesaj
     tüketicilerini drain et),
  3. in-flight işi süreli bekle (`context.WithTimeout`, ortamın kill-timeout'unun
     altında),
  4. bağımlılıkları kapat (DB pool, bus), çık.

  Bu sıra kodda tek bir yerde, okunur şekilde durur.
- Sağlık uçları iki tane: `/healthz` = süreç canlı (bağımlılık kontrolü yapmaz),
  `/readyz` = trafiğe hazır (DB/bus erişilebilir). Karıştırılırsa DB kesintisi tüm
  replikaları restart döngüsüne sokar.
- Süreç ölürken iz bırakır: `GOTRACEBACK=all`, stderr toplanır. Sessiz ölüm yok.

## Goroutine disiplini
Üretimdeki bir numaralı sızıntı kaynağı. Kural: her goroutine'in sahibi, bitiş
koşulu ve hata yolu vardır.
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
- Testler `-race` ile; `goleak` ile goroutine sızıntısı testi, özellikle shutdown
  testi.

## Context
- Sınırdan giren her fonksiyon ctx alır, aşağı geçirir. `context.Background()`
  yalnızca main/test; `context.TODO()` commit edilmez.
- ctx struct'ta saklanmaz. Saklanırsa iptal semantiği kaybolur.
- Context'e yalnızca request-scoped meta (correlation id, principal). Logger, DB,
  config context'te taşınmaz.
- Her dış çağrının zaman sınırı vardır: `context.WithTimeout` veya client-level
  timeout. `http.DefaultClient` (timeout'suz) yasak.
- Arka plan işi (relay, cron) request ctx'ine bağlanmaz; kendi ömür ctx'i vardır.
  Aksi halde istek bitince iş yarım kalır.

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
  döner, loglamaz. Üç katmanda aynı hata üç log satırı = gerçek olayı gizler.
- Kütüphane katmanı log çağırmaz; hata döner. Loglamak uygulama katmanının işi.

## Kapalı tip kümesi
- Üyeleri belli bir tip kümesi (ör. mesaj ya da event türleri) interface ile
  ifade ediliyorsa interface'e `//sumtype:decl` yazılır ve en az bir unexported
  metodu olur. `gochecksumtype` o interface üzerindeki her type switch'te eksik
  case'i yakalar; `default` dalı eksik case'in yerini tutmaz.

## Panic ve recover
Panic servisi kapatmaz. `recover` yalnızca kendi goroutine'indeki panic'i yakalar;
`recover`'ı olmayan bir goroutine'de çıkan panic bütün süreci düşürür.
- Her goroutine'in girişinde (`errgroup`'a verilen fonksiyonlar dahil) ve her
  istek ya da mesaj handler'ında `recover` vardır. `net/http` panic'i yakalar ama
  yalnızca bağlantıyı keser; hata cevabı, log ve metrik için middleware yazılır.
- Yakalanan panic: stack loglanır, metrik artar, panic `error`'a çevrilip
  goroutine'in sahibine döner; istek hata cevabıyla biter. Servis ayakta kalır.
- Panic saklanmaz: goroutine kendini sessizce yeniden başlatıp devam etmez; hatayı
  sahibi görür ve karar verir.
- `recover` ile hata akışı kurulmaz: beklenen hata `error` döner; nil pointer'ı
  recover'la yakalayıp normal akışa dönmek bug'ı gizlemektir.
- `recover` her ölümü durdurmaz: `concurrent map writes` gibi runtime fatal
  error'lar ve OOM süreci yine düşürür. Onlara karşı `-race` testleri ve
  `GOMEMLIMIT`.

## Dış bağımlılıklar: timeout, retry, devre kesici
- Retry yalnızca idempotent işlemde; üst sınır (deneme sayısı VE toplam süre),
  exponential backoff, jitter. Sınırsız retry sessiz ölümdür; retry her denemeyi
  değil sonucu loglar.
- Bağımlılık uzun süre düşükse devre kesici veya en azından hızlı-başarısızlık;
  her isteğin timeout'a kadar beklemesi goroutine ve bağlantı biriktirir.
- Bağlantı havuzları sınırlı ve config'ten: `sql.DB.SetMaxOpenConns`/
  `SetMaxIdleConns`/`SetConnMaxLifetime`; `http.Transport.MaxIdleConnsPerHost`.
  Varsayılanlar üretim için değildir.
- Süre ölçümü `time.Since` (monotonic). Zaman damgası UTC.

## Gözlemlenebilirlik
- Log: `log/slog`, JSON, tek logger `run`'da kurulur ve bağımlılık olarak geçilir.
  `fmt.Println`/`log.Printf` üretim kodunda yok. Log seviyesi config'ten,
  runtime'da değiştirilebilir.
- Her log satırında correlation id; ctx'ten gelir, handler'da üretilir veya
  header'dan alınır.
- Metrik: Prometheus; her worker için işlenen/hata/süre histogramı; her
  kuyruk/kanal için derinlik ve lag; her bağımlılık için çağrı süresi ve hata
  oranı. Ölçek ve alarm bu metriklere bağlanır, CPU/RAM'e değil.
- Trace: OpenTelemetry; en az sınırdaki span + dış çağrı span'leri.
- `net/http/pprof` üretimde açık, iç ağa sınırlı. Bellek sızıntısını tahminle
  değil heap profile ile bulursun.
- Bellek: `GOMEMLIMIT` container/VM limitinin altına set edilir. `GOMAXPROCS`
  elle ayarlanmaz; Go 1.25+ cgroup CPU quota'sını kendisi okur.

## Config
- Tek kaynak: env veya dosya, `run` başında bir struct'a parse edilir ve
  doğrulanır. Kod içinden `os.Getenv` çağrısı yok.
- Sır (parola, token) loglanmaz; config struct'ın `String()`/`LogValue()`'su
  maskeler.
- Varsayılanlar üretim değeri değil, geliştirme değeridir; üretimde her kritik
  değer açıkça set edilir (timeout, pool, worker sayısı).

## Test
- `go test -race ./...` her zaman; CI'da kapatılmaz.
- Bağımlılık gerektiren testler gerçek bağımlılıkla çalışır (testcontainers ya da
  embedded sunucu). Mock'lu DB testi DB bug'ı bulmaz.
- Shutdown testi vardır: servisi başlat, iş ver, SIGTERM/ctx iptal; hiçbir
  goroutine kalmadığını ve in-flight işin tamamlandığını doğrula.
- Interface yalnızca test için açılmaz; önce somut tip, gerçek ikinci
  implementasyon gelince interface.

## Bağımlılık ve derleme
- `go.mod`/`go.sum` commit; `go mod tidy` temiz; `replace` gerekçeli ve geçici.
- Eklemeden önce stdlib ve `golang.org/x`'e bak; 20 satırlık işe kütüphane
  eklenmez.
- Tek Go sürümü (`go` direktifi); CI ve geliştirme ortamı aynı sürüm.
- `go.mod`'a `toolchain` direktifi yazılmaz. Go sürümü devshell'den gelir;
  `GOTOOLCHAIN=auto` olduğu için devshell'dekinden yeni bir direktif go'ya başka
  bir toolchain indirtir.
- Binary `CGO_ENABLED=0` ile statik derlenir; cgo açılırsa gerekçe yazılır.
  Testler cgo'lu koşar: `-race` cgo ister.
- Binary'ye sürüm/commit `-ldflags "-X"` ile gömülür, `/version` veya log'da
  görünür.
