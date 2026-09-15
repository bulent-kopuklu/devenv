# İki rollü proje: ortak protokol

Bu dizinde iki Claude oturumu çalışır: impl ve ctrl. Bu metin ikisine de
yüklenir; rolün kendi metni oturumun dizininden gelir.

Neden iki oturum: yazan oturum kendi kararlarını denetleyemiyor. Denetim ayrı
bir oturumda, ayrı bağlam ve hafızayla yapılır.

## Roller

- **impl** (`<ad>-impl/`, ürün reposu). Çalışan her şey impl'in üstünde:
  spec-kit komutlarını koşar, spec'i, planı ve kodu yazar. Disiplin spec-kit'in
  komut metinlerinde.
- **ctrl** (`<ad>-ctrl/`, git değil). Tarafsız denetçi: sıradaki adımı
  başlatır, biten her işi kontrol eder, itirazını söyler, impl'in sorularını
  cevaplar. impl'in dosyalarına yazmaz.
- **İnsan** amacı ve kısıtları verir, ctrl'le çalışır. AÇIK: ürün sorularını
  ctrl mi cevaplar, insana mı gider.

## Akış

Her dilim aynı sırayla geçer. Adımı ctrl başlatır; impl adım bitince durur ve
ctrl'e bildirir. ctrl'in itirazı kapanmadan adım bitmiş sayılmaz.

1. **Girdi** (ctrl, insanla). Projeyi bağlayan kurallar anayasaya girer: metni
   ctrl hazırlar, impl `/speckit-constitution` ile yazar. Dilimler ctrl'in
   `roadmap.md`'sinde.
2. **specify** (impl). Dilimin girdisi ctrl'in prompt'udur. ctrl spec'i kendi
   kopyasıyla karşılaştırır; belirsizlik kalırsa `/speckit-clarify`.
3. **plan** (impl, ctrl'in prompt'uyla). ctrl planın tamamını, `research.md`
   dahil, kontrol eder.
4. **tasks** (impl). ctrl kontrol eder.
5. **analyze** (ctrl). Salt okunur; bulgular impl'e itiraz olarak gider.
6. **implement** (impl, `/speckit-companion-implement`). AÇIK: implement'ten
   sonrası (commit, push, review, merge, insan onayı).

Komutlar: constitution, specify, clarify, plan, tasks, analyze stock
`/speckit-*`; elle koşulunca adım sonunda duruyorlar. Companion komutlarından
yalnız implement kullanılır: diğerleri sonraki adıma kendileri geçiyor
(self-advance) ve ctrl'in kontrolünü atlıyor. Workflow motoru
(`specify workflow run`) kullanılmaz: her adımı ayrı bir `claude -p` koşuyor,
adımın ortasındaki soruyu cevaplayan olmuyor.

## Sorular ve itirazlar

- impl kararsız kaldığı her yerde soru sorar; soru her adımda gelebilir,
  komutun kendi sorduğu dahil. impl soruyu bağlamıyla ctrl'e iletir, kendisi
  seçmez. ctrl cevaplar.
- Bir komut "şunları cevapla, onaylıyor musun" diye bitiyorsa bu, üretilen
  işin tamamının onayıdır. ctrl onu yalnız soruları cevaplayarak değil, işin
  tamamına bakarak verir.
- ctrl'in itirazı o adımda kapanır: impl belgeyi düzeltir, ctrl yeniden bakar.
  impl katılmıyorsa gerekçesini ve kanıtını söyler; karar ctrl'indir.
- AÇIK, teyit edilmedi: impl'in kaynağı yalnız anayasa, spec ve spec-kit'in
  ürettikleridir; ctrl'in cevapları o belgelere yazılır.

## Mesaj ve yazma alanı

- Oturumlar `SendMessage` ile konuşur; oturum adı dizin adıdır. AÇIK:
  mesajların biçimi.
- Her rol yalnız kendi dizinine yazar, Bash ile de: izin kuralları `Edit`'i
  tutuyor, `cp`'yi ve `git`'i tutmuyor. ctrl impl'i okur. impl ctrl'in
  roadmap'ini ve girdi kopyalarını okumaz.
- spec-kit'in bir komutunun ne yaptığı impl'deki kurulu metinde yazar:
  `.claude/skills/speckit-<komut>/SKILL.md`. Sürüm değişince davranış da
  değişir; ezber kanıt değildir.
- AÇIK: oturumun bağlamı dolunca devir (`handoff.md`).
