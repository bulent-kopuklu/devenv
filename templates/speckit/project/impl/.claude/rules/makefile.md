# Makefile

İnsan terminalde yalnız `make <hedef>` yazar; hangi aracın hangi parametreyle
koştuğunu Makefile bilir. Kökteki `Makefile` ürünündür. Proje onu reçetesiz
bir iskelet olarak alır: parametreler, doğrulamaları ve toplu hedefler hazırdır,
toplu hedefler bileşen bağlanana kadar boş geçer. Her bileşenin reçetesini sen
eklersin.

## Hedefler

| hedef | ne yapar |
|---|---|
| `build` | varsayılan hedef; bütün bileşenleri derler |
| `test` | unit ve contract testleri |
| `test-integration` | integration testleri |
| `test-evidence` | evidence senaryoları |
| `bench` | bench'ler; kapıya girmez |
| `lint` | formatter denetimi ve linter'lar |
| `gate` | sırayla `build`, `lint`, `test`, `test-integration`, `test-evidence` |
| `dist` | release derler, teslim edilenleri `dist/<target>/` altına toplar |
| `clean` | `build/`'i siler |
| `distclean` | `clean`'e ek olarak `dist/`'i ve bileşenlerin bağımlılık dizinlerini siler |

Her hedefin bileşen başına bir hâli vardır: `<hedef>-<ad>` (`build-api`,
`test-integration-api`). Toplu hedef, bileşenlerin hedeflerini çağırır.

## Parametreler

| parametre | değerler |
|---|---|
| `VARIANT` | `debug` (varsayılan), `release` |
| `TARGET` | `host` (varsayılan), `aarch64`, `armv7` |
| `COMPONENTS` | varsayılan `components/` altındaki bütün bileşenler; boşlukla ayrılmış bir alt küme verilebilir |

Geçersiz bir `VARIANT` ya da `TARGET` değeri make başlamadan hata verir.
Testler `TARGET=host`'ta koşar; başka bir hedefte test istenince make hata
verir.

## Çıktının yeri

- Derleme çıktısı `build/<target>/<variant>/`, teslim edilen binary'ler
  `$(BIN)` = `build/<target>/<variant>/bin/` altındadır. `dist` bu `bin/`'i
  toplar.
- Test ve kapı koşularının çıktısı `$(RUNS)` altında, koşu başına bir
  dizindedir. Varsayılanı repo içindeki `runs/`; git dışındadır. `clean` ve
  `distclean` ona dokunmaz, yalnız insan temizler.

## Bileşeni bağlamak

1. Bir bileşeni `components/<ad>/` altında açtığın commit'te onu Makefile'a
   bağlarsın: `build-<ad>`, `lint-<ad>` ve bileşenin testi olan her tür için
   o türün hedefi; toplu hedef bu hedefleri çağırır.
2. Reçete bileşenin kendi aracını çağırır (`go`, `cargo`, `cmake`, `npm`,
   `uv`); araçlar devshell'den gelir. Dilin reçeteleri (bayraklar, cross
   hedef, çıktının `$(BIN)`'e gelmesi) `.claude/rules/<dil>.md`'nin Makefile
   bölümündedir.
3. Bileşenin testi olmayan türün hedefine bileşeni bağlamazsın; hiçbir
   bileşenin o türde testi yoksa hedef boş geçer.
4. Tablodaki hedeflere bileşen bağlamak ve bileşene özgü bir adım eklemek
   plan'ın işidir. Tabloda olmayan bir hedef adı ya da parametre gerekiyorsa
   plan'da yazılır ve proje sahibine sorulur.
