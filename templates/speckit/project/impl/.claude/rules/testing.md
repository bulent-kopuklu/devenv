# Test

Bir bileşenin testlerinin yeri ve bir story'nin testlerinin ne zaman yazıldığı.
Dilden bağımsızdır; dilin karşılıkları `.claude/rules/<dil>-testing.md`'dedir
(Go: `go-testing.md`).

## Temel ilke

Bir testin yeri, neyi ölçtüğüne göre belirlenir; dokunduğu altyapıya göre değil.

## Story story çalışma

- Task'lar user story'lere göre sıralıdır; her story bir fazdır.
- Story fazında önce kod yazılır. Kod yazılırken bir şeyden emin olmak
  gerekirse unit testle sınanır.
- Story'nin kodu bitince story'nin acceptance senaryoları ve o story için
  gereken Success Criteria'lar acceptance testi olarak yazılır. Bir SC
  davranışı birden çok story'ye dayanıyorsa testi, plan.md'nin SC tablosunda
  o davranışın satırındaki son story'nin fazında yazılır; SC dosyası fazdan
  faza büyür.
- Kod yazılmadan testi yazılmaz. Ortada olmayan bir şeyin testi varsayımla
  yazılır, ürünün küçük bir kısmını ölçer ve sonraki iş ürünü yazmak değil
  kırmızıyı yeşile çevirmek olur.
- Hata bulununca kod ortadadır; önce onu yeniden üreten test yazılır (Hata).
- Bir acceptance testinin hangi SC'ye ya da story'ye ait olduğu adından
  bellidir. Sonraki bir fazda kırmızı yanarsa test değiştirilmez, kod
  düzeltilir; testin iddiası yalnız spec cümlesi değişince değişir.
- Her story'nin sonunda gate o an var olan testleri koşar: US2 bitince US1'in
  ve US2'nin testleri.
- plan.md'nin SC tablosu her SC davranışı için davranışı getiren user
  story'leri, acceptance testini ve paket düzeyindeki testi yazar.

## Unit testler: kodun yanında

- Paketin iç yapısını sınayan test paketinde kalır.
- Dosya, sınadığı kodun adını alır.
- Veritabanı ya da broker açması onu başka bir tür yapmaz: etiketsizdir, her
  koşuda koşar.
- Bir SC'nin mekanizmasını paket içinde ölçen test de burada kalır;
  plan.md'nin SC tablosunda "paket düzeyinde" sütununda anılır.

## Acceptance: SC ve US senaryoları ayrı ağaçta

- Yer: `components/<ad>/tests/acceptance/`. `tests/` ürüne derlenmez.
- Tek ve düz bir dizin; katman dizini yok.
- Success Criteria:
  - SC başına tek dosya: `s<spec>-sc-<NNN>-<SC'den türeyen ad>` (s001 = spec 001).
  - Dosyanın başında SC'nin spec'teki cümlesi.
  - SC'nin her davranışı ayrı bir test; davranış, SC'nin bir cümlesi ya da
    virgülle ayrılan bir hâlidir.
  - İki SC'yi ölçen test ilk SC'nin dosyasındadır; başlık öbür SC'yi anar.
- User story:
  - `s<spec>-us-<NNN>-<story'den türeyen ad>`; başında story'nin içeriği ve
    acceptance senaryoları.
  - SC dosyasındaki test US dosyasına kopyalanmaz; US dosyası SC dosyalarını
    yalnız anar. Aynı test iki kez koşmaz.
  - Hiçbir story'ye bağlanmayan test içeriğine en yakın story'nin dosyasına
    gider.
- Her SC'nin ve her US'nin kendi dosyası vardır; dosyalar numara sırasıyla,
  arada numara atlanmadan durur. Bir SC'nin ya da US'nin testi başka bir
  dosyadaysa kendi dosyası onu anar.
- Black-box: senaryo ürünü public API'yle sürer; sonucu store'dan (kendi
  bağlantısıyla ya da SQL'le), broker'dan ve ürünün görünürlük yüzeyinden
  okur. Ürünün iç paketlerinin dışarı açık adları kullanılabilir (dil
  dosyası); iç alana erişim ve ürüne test hook'u yok.
- Evidence ayrımı yok: process'i öldüren (`SIGKILL`), durduran (`SIGSTOP`) ya
  da ağını kesen davranışlar da acceptance'tadır; müdahaleyi test yapar.
- Ürünün birden çok instance'ını isteyen testte her instance ayrı bir
  process'tir.
- Her senaryo bir şey kanıtladığını kendisi denetler (ör. hiç unit el
  değiştirmediyse "the test proves nothing" ile düşer); denetçilerin negatif
  kontrolleri vardır.
- Uzun ölçüm günlük koşudan ayrılır (SC-005'in ~17 dakikalık boş yük testi).
- integration diye bir tür yok. Bileşen başka bileşenlere bağımlıysa
  acceptance testi koşarken onlar da, veritabanı ve broker gibi, ayağa kalkar.
- Acceptance yalnız spec'in US senaryoları ve SC'leri içindir. Implementation
  sırasında bulunan bir hatanın testi acceptance dosyasına yazılmaz.

## Sistem senaryosu: hatadan doğan test

- Hata önce en alçak düzeyde test edilir (Hata). Çiğnenen söz yalnız sistem
  düzeyinde görülebiliyorsa (birden çok process, ağ kesintisi, dış sistemin
  kaybı gibi) buna ek olarak bir sistem senaryosu yazılır.
- Yer: `components/<ad>/tests/scenario/`; tek ve düz bir dizin.
- Dosya: `s<spec>-ss-<NNN>-<hatadan türeyen ad>`. `<spec>` hatanın bulunduğu
  implementation'ın spec'idir; `<NNN>` o spec'in bu dizindeki sıradaki
  numarasıdır.
- Dosyanın başında: gözlenen belirti, belirtiyi doğuran koşul (müdahale),
  çiğnenen sözün spec'teki cümlesi, bug kaydının yeri (`.specify/bugs/<slug>/`).
- Yazılışı acceptance'la aynıdır: black-box, müdahaleyi test yapar, birden
  çok instance ayrı process'tir, kanıtladığını kendisi denetler, denetçinin
  negatif kontrolü vardır, uzun ölçüm günlük koşudan ayrılır.
- Plan ve tasks'ta yer almaz; kaydı bug dosyasındadır.

## Contract: sözleşme belgesinin testi

- `tests/contract/`: `contracts/` belgesinin altın dosya testleri. Altın
  dosyalar ürünün bir sürümünün tele yazdığı mesajların dondurulmuş
  örnekleridir; test bugünkü kodun onlarla uyumlu kaldığını sınar (okuma ve
  yeniden yazma, bilinmeyen alan, eksik alan).
- Container açmaz.

## Yardımcılar: yerini kimin kullandığı belirler

| kim kullanıyor | yer |
|---|---|
| ürün paketlerinin testleri de | ürünün kendi ağacında, test yardımcılarının yerinde (dil dosyası) |
| tek bir paketin sahtesi | paketin yanında |
| yalnız acceptance ve sistem senaryoları | `tests/` altında, ne yaptığını söyleyen pakette |

- Bir yardımcının ikinci bir kullanıcısı çıkarsa yukarı taşınır; kopyalanmaz.
- Acceptance ve sistem senaryosu yardımcıları ne yaptığını söyleyen ayrı
  paketlerde durur; test dosyalarının arasında araç kodu durmaz.
- Bileşenler arasında kopya serbesttir; her bileşen kendi ihtiyacını kendi
  içinde çözer.

## Fixture'lar: test ağacında

- Test verisi ürün ağacında durmaz: `tests/fixtures/<konu>/<sürüm>/`.
- Sürüm dizini silinmez; yeni sürüm yanına eklenir ve yeni kod eski sürümün
  dosyalarını da okumak zorunda kalır.

## Hata

- Bir kez geçmiş bir test kırmızı yanarsa bu bir bulgudur; tekrar koşmak onu
  kapatmaz.
- Önce hatanın üretilebildiği en alçak düzeyde, düzeltilmemiş kodda kırmızı
  yanan test; sonra düzeltme. Kırmızı çıktı commit mesajına girer.
- Düzeltme önerisi önce spec ve plan'la çatışmazlık için denetlenir; seçeneği
  insan seçer.
- Implementation'a geçildikten sonra spec, plan, research ve tasks'a
  dokunulmaz. Hatanın ve kararın kaydı bug dosyasına (`.specify/bugs/<slug>/`)
  gider.
- Hata unit testle üretilir; üretilemiyorsa ya da çiğnenen söz yalnız sistem
  düzeyinde görülebiliyorsa sistem senaryosu yazılır. Acceptance dosyasına
  hata testi eklenmez.

## Evidence

- evidence ürünü black-box sınar: public API'yle oluşabilecek her race
  condition ve her felaket senaryosu.
- US ve SC davranışları evidence'ta değil acceptance'tadır.

## Ayıklama

- Spec'in sonunda gereksiz kalan testler ayıklanır. Acceptance testi
  ayıklanmaz: SC'nin ve US'nin testi, aynı davranışı daha alçak düzeyde ölçen
  bir test olsa da kalır.
- Ayıklama denetçi başınadır: bir senaryo birden çok şey ölçebilir. Bir
  denetçi, aynı davranışı iddianın kendisini ölçerek daha alçak ya da aynı
  düzeyde sınayan bir test varsa gereksizdir. Silmeden önce mekanizma bozulur
  (düzeltme geri alınır ya da denetçinin negatif kontrolü uygulanır) ve kalan
  testin kırmızı yandığı gösterilir; çıktı silme commit'ine yazılır. Açık
  bulgusu olan ya da başka bir feature'ın plan.md'sinin dayandığı test
  silinmez.
