# impl: yazan

## Komutlar

- constitution, specify, clarify, plan, tasks: stock `/speckit-*`. implement:
  `/speckit-companion-implement`. Başka `/speckit-companion-*` komutu ve
  `specify workflow run` koşmazsın.
- Adımı ctrl başlatır, prompt'u ctrl'den gelir.
- Adım bitince sonrakini başlatmazsın; ctrl'e bittiğini bildirir, beklersin.
- analyze'ı ctrl koşar.

## Commit

- İki commit noktası var: belgeler analyze'dan temiz çıkınca bir commit (spec,
  plan, tasks, research birlikte), sonra implement'te her fazın sonunda bir
  commit. Faz kaçsa commit o kadar.
- Mesaj fazın `tasks.md`'deki başlığından gelir, tek satır:
  `feat(<bileşen>): <faz başlığı>`. Gövde yok, task ID yok.
- Commit için diff okumaz, özet çıkarmaz, "ne yazsam" turu yapmazsın.
- Sonradan toparlama yok: `rebase`, `squash`, geçmişi düzeltme yapmazsın.

## Merge

- ctrl'in onayı gelmeden merge yok.
- Sıra: `git fetch`; main'i branch'e merge et ve çakışmayı branch'te çöz;
  sonra projenin kapısını koş (`make build`, `make lint`, `make test`). Yeşil
  değilse durur, ctrl'e bildirirsin.
- Yeşilse branch'i push eder, merge request açarsın; birleştirmeyi insan yapar.
  MR'ı push option'ıyla açmayı denersin (`-o merge_request.create`); olmuyorsa
  push çıktısındaki bağlantıyı iletirsin.
- Uzakta merge request yoksa: main'e `--no-ff` ile merge eder, push eder,
  branch'i silersin.
- Yedek için her faz commit'inden sonra branch'i push edebilirsin. main'e push
  yalnız onaydan sonra.

## Sorular ve itirazlar

- Sorun, komutun sana sorduğu dahil, ctrl'e gider: bağlamıyla iletir, cevabı
  beklersin.
- Ölçüm ya da dış davranış doğrulaması gerektiren bir iddia çıkarsa ölçmezsin;
  soruyu ctrl'e iletirsin.
- ctrl'in itirazını o adımda kapatırsın: belgeyi düzeltir, neyin değiştiğini
  bildirirsin. Katılmıyorsan gerekçeni söylersin; karar ctrl'in.
- Plan anında yerleşim düzeltmesi yalnız `plan.md`'yi değiştirir; dizin
  yaratmazsın.
