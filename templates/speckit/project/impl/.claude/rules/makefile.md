# Makefile

İnsan terminalde yalnız `make <hedef>` yazar; hangi aracın hangi parametreyle
koştuğunu Makefile bilir. İki katman vardır. Kökteki `Makefile` arayüzü taşır
ve bir hedefi `COMPONENTS`'teki her bileşene `$(MAKE) -C components/<ad> <hedef>`
ile indirir; reçete taşımaz. Her bileşenin reçeteleri kendi
`components/<ad>/Makefile`'ındadır. Bileşen eklemek kök Makefile'ı
değiştirmez.

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
| `distclean` | `clean`'e ek olarak `dist/`'i siler ve bileşenlerin `distclean`'ini çağırır |

Tek bileşen için hedef `COMPONENTS` ile daraltılır: `make test COMPONENTS=api`.

## Parametreler

| parametre | değerler |
|---|---|
| `VARIANT` | `debug` (varsayılan), `release` |
| `TARGET` | `host` (varsayılan), `aarch64`, `armv7` |
| `COMPONENTS` | varsayılan `components/` altında `Makefile`'ı olan bütün bileşenler; boşlukla ayrılmış bir alt küme verilebilir |
| `RUNS` | koşu çıktısının kökü; env'den gelir |
| `EVIDENCE` | `short`, `full`; evidence senaryolarını seçer |

Geçersiz bir `VARIANT` ya da `TARGET` değeri make başlamadan hata verir.
Testler `TARGET=host`'ta koşar; başka bir hedefte test istenince make hata
verir.

## Bileşenin Makefile'ı

1. Bir bileşeni `components/<ad>/` altında açtığın commit'te onun
   `Makefile`'ını yazarsın. `build`, `test`, `test-integration`,
   `test-evidence`, `bench`, `lint` ve `distclean` hedeflerinin hepsini
   tanımlar; bileşenin testi olmayan türün ve işi olmayan hedefin reçetesi
   boştur (`@:`).
2. Kök şu değişkenleri export eder; bileşen onları kullanır, kendisi
   tanımlamaz: `VARIANT`, `TARGET`, `BUILD` (derleme kökü), `BIN` (teslim
   edilen binary'lerin yeri), `TEST_RUN` (koşu dizini). Üç yol da mutlaktır.
   `EVIDENCE` komut satırından gelir.
3. Reçete bileşenin kendi aracını çağırır (`go`, `cargo`, `cmake`, `npm`,
   `uv`); araçlar devshell'den gelir. Dilin reçeteleri (bayraklar, cross
   hedef, çıktının `$(BIN)`'e gelmesi) `.claude/rules/<dil>.md`'nin Makefile
   bölümündedir.
4. Tablodaki hedeflerin reçetesini yazmak ve bileşene özgü bir adım eklemek
   plan'ın işidir. Tabloda olmayan bir hedef adı ya da parametre gerekiyorsa
   plan'da yazılır ve proje sahibine sorulur.

## Çıktının yeri

- Derleme çıktısı `$(BUILD)/<target>/<variant>/`, teslim edilen binary'ler
  `$(BIN)` = `build/<target>/<variant>/bin/` altındadır. `dist` bu `bin/`'i
  toplar.
- evidence koşularının çıktısı `$(TEST_RUN)` altındadır; unit ve integration
  terminale yazar. Bir make çağrısı tek bir koşu dizini açar:
  `$(RUNS)/<proje>/<zaman>-<hedef>/`. gate'in alt make'leri aynı dizini
  kullanır; her bileşen `$(TEST_RUN)/<ad>/<hedef>` altına yazar.
- `RUNS` env'den gelir, verilmezse `$XDG_STATE_HOME/runs`, o da yoksa
  `~/.local/state/runs`'tır; yeniden başlatmada silinmez. CI'da işin artifact
  dizini verilir. `clean` ve `distclean` ona dokunmaz, yalnız insan temizler.
- Reçeteler POSIX `sh` ile koşar; bash'e özgü bir şey kullanmaz.
