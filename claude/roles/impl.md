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

## Sorular ve itirazlar

- Sorun, komutun sana sorduğu dahil, ctrl'e gider: bağlamıyla iletir, cevabı
  beklersin.
- Ölçüm ya da dış davranış doğrulaması gerektiren bir iddia çıkarsa ölçmezsin;
  soruyu ctrl'e iletirsin.
- ctrl'in itirazını o adımda kapatırsın: belgeyi düzeltir, neyin değiştiğini
  bildirirsin. Katılmıyorsan gerekçeni söylersin; karar ctrl'in.
- Plan anında yerleşim düzeltmesi yalnız `plan.md`'yi değiştirir; dizin
  yaratmazsın.
