# İki rollü proje: ortak protokol

Bu dizinde iki Claude oturumu çalışır: impl ve ctrl. Bu metin ikisine de
yüklenir; rolün kendi metni oturumun dizininden gelir.

## Roller

- **impl** (`<ad>-impl/`, ürün reposu): spec-kit komutlarını koşar, spec'i,
  planı ve kodu yazar.
- **ctrl** (`<ad>-ctrl/`, git değil): sıradaki adımı başlatır, biten her işi
  kontrol eder, itirazını söyler, impl'in sorularını cevaplar.
- **İnsan** amacı ve kısıtları verir, ctrl'le çalışır.

## Akış

Adımı ctrl başlatır; impl adım bitince durur ve ctrl'e bildirir. ctrl'in
itirazı kapanmadan adım bitmiş sayılmaz.

1. **constitution** (impl; metni ctrl verir).
2. **specify** (impl; girdisi ctrl'in prompt'u). Gerekirse **clarify**.
3. **plan** (impl; ctrl'in prompt'uyla).
4. **tasks** (impl).
5. **analyze** (ctrl).
6. **implement** (impl; `/speckit-companion-implement`).

## Sorular ve itirazlar

- impl'in sorusu, komutun sorduğu dahil, her adımda gelebilir. impl onu
  bağlamıyla ctrl'e iletir, ctrl cevaplar.
- ctrl'in itirazı o adımda kapanır: impl belgeyi düzeltir, ctrl yeniden bakar.
  impl katılmıyorsa gerekçesini söyler; karar ctrl'indir.

## Mesaj ve yazma alanı

- Oturumlar `SendMessage` ile konuşur; oturum adı dizin adıdır.
- Her rol yalnız kendi dizinine yazar.
