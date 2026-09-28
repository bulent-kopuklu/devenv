# Makefile

İnsan terminalde yalnız `make <hedef>` yazar; hangi aracın hangi parametreyle
koştuğunu Makefile bilir. İki katman vardır. Kökteki `Makefile` arayüzü taşır
ve bir hedefi `COMPONENTS`'teki her bileşene `$(MAKE) -C components/<ad> <hedef>`
ile, evidence hedeflerini `evidence/Makefile`'a indirir; reçete taşımaz. Her
bileşenin reçeteleri kendi `components/<ad>/Makefile`'ında, her evidence
dizininin reçeteleri kendi `evidence/<dizin>/Makefile`'ındadır. Bileşen ya da
evidence dizini eklemek kök Makefile'ı ve `evidence/Makefile`'ı değiştirmez.

## Hedefler

| hedef | ne yapar |
|---|---|
| `build` | varsayılan hedef; bütün bileşenleri ve evidence'ın probe'larını derler |
| `test` | unit ve contract testleri |
| `test-integration` | integration testleri |
| `bench` | bench'ler; kapıya girmez |
| `lint` | bileşenlerde ve evidence'ta formatter denetimi ve linter'lar |
| `evidence:<ad>` | bir bileşenin (`evidence/<ad>/`) ya da sistemin (`evidence/systems/<ad>/`) evidence'ı |
| `evidence:all` | bütün evidence dizinleri |
| `gate` | sırayla `build`, `lint`, `test`, `test-integration`, `evidence:all` |
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
| `SCENARIO` | tek bir evidence senaryosunun adı; verilmezse `EVIDENCE`'ın seçtiği hepsi |

Geçersiz bir `VARIANT` ya da `TARGET` değeri make başlamadan hata verir.
Testler ve evidence `TARGET=host`'ta koşar; başka bir hedefte istenince make
hata verir.

## Bileşenin Makefile'ı

1. Bir bileşeni `components/<ad>/` altında açtığın commit'te onun
   `Makefile`'ını yazarsın. `build`, `test`, `test-integration`, `bench`,
   `lint` ve `distclean` hedeflerinin hepsini tanımlar; bileşenin testi
   olmayan türün ve işi olmayan hedefin reçetesi boştur (`@:`).
2. Kök şu değişkenleri export eder; bileşen onları kullanır, kendisi
   tanımlamaz: `VARIANT`, `TARGET`, `BUILD` (derleme kökü), `BIN` (teslim
   edilen binary'lerin yeri), `TEST_RUN` (koşu dizini). Üç yol da mutlaktır.
3. Reçete bileşenin kendi aracını çağırır (`go`, `cargo`, `cmake`, `npm`,
   `uv`); araçlar devshell'den gelir. Dilin reçeteleri (bayraklar, cross
   hedef, çıktının `$(BIN)`'e gelmesi) `.claude/rules/<dil>.md`'nin Makefile
   bölümündedir.
4. Tablodaki hedeflerin reçetesini yazmak ve bileşene özgü bir adım eklemek
   plan'ın işidir. Tabloda olmayan bir hedef adı ya da parametre gerekiyorsa
   plan'da yazılır ve proje sahibine sorulur.

## evidence'ın Makefile'ları

1. `evidence/Makefile` devenv'den gelir ve dilsizdir: `build` ve `lint`'i her
   evidence dizinine indirir, `evidence:<ad>`'ı adın dizinine, `evidence:all`'u
   hepsine. Olmayan bir ad hata verir.
2. Bir evidence dizinini (`evidence/<bileşen>/` ya da
   `evidence/systems/<ad>/`) açtığın commit'te onun `Makefile`'ını yazarsın.
   `build`, `lint` ve `run` hedeflerinin hepsini tanımlar; işi olmayanın
   reçetesi boştur (`@:`).
   - `build`: dizinin probe'larını derler, `$(OUT)/bin/`'e yazar.
   - `lint`: probe'ların ve script'lerin lint'i.
   - `run`: probe'ları `$(MAKE) build OUT=$(RUN)` ile koşu dizinine derler,
     senaryoları koşar; çıktısı `$(RUN)` altındadır.
   `OUT` ve `RUN`'ı `evidence/Makefile` verir; `SCENARIO` ve `EVIDENCE`
   komut satırından ortam değişkeni olarak gelir.
3. Sistem dizininin probe'u yoktur; kullandığı bileşenlerin probe'larını
   onların Makefile'ıyla derletir: `$(MAKE) -C ../../<bileşen> build OUT=$(RUN)/<bileşen>`.
   Sistemin tanımı bu Makefile'dır: hangi bileşenlerin probe'larını kullandığı.

## Çıktının yeri

- Derleme çıktısı `$(BUILD)/<target>/<variant>/`, teslim edilen binary'ler
  `$(BIN)` = `build/<target>/<variant>/bin/` altındadır. `dist` bu `bin/`'i
  toplar. evidence'ın `build`'i probe'ları `$(BUILD)/evidence/<dizin>/`'e
  yazar; onlar `$(BIN)`'e ve `dist`'e girmez.
- evidence koşularının çıktısı `$(TEST_RUN)` altındadır; unit ve integration
  terminale yazar. Bir make çağrısı tek bir koşu dizini açar:
  `$(RUNS)/<proje>/<zaman>-<hedef>/` (hedefteki `:` `-` olur). gate'in alt
  make'leri aynı dizini kullanır; her evidence dizini `$(TEST_RUN)/<dizin>`
  altına yazar.
- `RUNS` env'den gelir, verilmezse `$XDG_STATE_HOME/runs`, o da yoksa
  `~/.local/state/runs`'tır; yeniden başlatmada silinmez. CI'da işin artifact
  dizini verilir. `clean` ve `distclean` ona dokunmaz, yalnız insan temizler.
- Reçeteler POSIX `sh` ile koşar; bash'e özgü bir şey kullanmaz.
