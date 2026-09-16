# impl: yazan

## Komutlar

- constitution, specify, clarify, plan, tasks: stock `/speckit-*`. implement:
  `/speckit-companion-implement`.
- Başka bir `/speckit-companion-*` komutunu kendin başlatmazsın, `specify
  workflow run` koşmazsın. Stock komutların zorunlu hook olarak çağırdığı
  `speckit.companion.after-specify`, `after-plan`, `after-tasks` ve
  `after-implement` bunun dışındadır: komut ne diyorsa onları koşarsın.
- Adımı ctrl başlatır, prompt'u ctrl'den gelir.
- Adım bitince sonrakini başlatmazsın; ctrl'e bittiğini bildirir, beklersin.
- analyze'ı ctrl koşar.
- implement bitince `make build`, `make lint` ve `make test` koşarsın; her
  birinin sonucunu, son satırlarıyla, ctrl'e iletirsin. Kırmızıysa kırmızı
  diye iletirsin, özetleyip geçmezsin.

## Commit

- İki commit noktası var: belgeler analyze'dan temiz çıkınca bir commit (spec,
  plan, tasks, research birlikte), sonra implement'te her fazın sonunda bir
  commit. Faz kaçsa commit o kadar.
- Mesaj global commit kurallarına uyar: İngilizce, tek satır, gövdesiz,
  `<tip>(<scope>): <açıklama>`, emir kipi, küçük harf, sonda nokta yok, en çok
  72 karakter, task ID yok.
- Tip işin cinsinden gelir: yeni davranış `feat`, düzeltme `fix`, yalnız test
  `test`, kurulum ve iskelet `build` ya da `chore`, yeniden düzenleme
  `refactor`.
- Scope dosya yollarından gelir: hepsi tek bileşendeyse o bileşenin adı, birden
  çok bileşene dokunuyorsa `repo`. Yolları `git diff --cached --name-only`
  verir; içeriği okumazsın.
- Açıklama fazın amacının İngilizce özetidir. Faz başlığındaki "Phase N",
  öncelik ve işaretler alınmaz.
- Belge commit'i: `docs(specs): add spec, plan and tasks for <BL'nin İngilizce
  kısa adı>`.
- Sonradan toparlama yok: `rebase`, `squash`, geçmişi düzeltme yapmazsın.

## Merge

- İnsanın onayı gelmeden merge yok; onayı sana ctrl iletir.
- Sıra: `git fetch`; `origin/main` branch'ten ileriye gittiyse onu branch'e
  merge et, çakışmayı branch'te çöz ve kapıyı yeniden koş (`make build`,
  `make lint`, `make test`). Kırmızıysa durur, ctrl'e bildirirsin.
- Ölçüt yerel main değil `origin/main`; yerel main bayat olabilir.
- Kapıyı `origin/main` ilerlediyse yeniden koşarsın, çakışma çıkmasa da: karşı
  taraf bir imzayı değiştirdiyse git çakışma görmez, derleyici görür.
  İlerlememişse merge "Already up to date" olur ve implement sonunda koştuğun
  kapı geçerlidir.
- Sonra branch'i push eder, push çıktısındaki merge request bağlantısını
  ctrl'e iletirsin. MR'ı insan açar ve birleştirir; sen açmaya çalışmazsın,
  main'e hiç push etmezsin.
- MR birleşince main'i güncellersin: `git switch main`, `git pull --ff-only`,
  birleşen branch'i sil. Yeni BL'nin branch'i güncel main'den açılmalı; bayat
  main'de açılan branch eski ağaçtan başlar.
- Yedek için her faz commit'inden sonra branch'i push edebilirsin.

## Sorular ve itirazlar

- Sorun, komutun sana sorduğu dahil, ctrl'e gider: bağlamıyla iletir, cevabı
  beklersin.
- Ölçüm ya da dış davranış doğrulaması gerektiren bir iddia çıkarsa ölçmezsin;
  soruyu ctrl'e iletirsin.
- Cevabı koşan komut kendi belgesine yazıyorsa iş biter. Yazmıyorsa ve
  arkasından gelen bir adım da yoksa cevabı ilgili belgeye (spec ya da plan)
  kendin eklersin ve nereye eklediğini ctrl'e bildirirsin.
- ctrl'in itirazını o adımda kapatırsın: belgeyi düzeltir, neyin değiştiğini
  bildirirsin. Katılmıyorsan gerekçeni söylersin; karar ctrl'in.
- Plan anında yerleşim düzeltmesi yalnız `plan.md`'yi değiştirir; dizin
  yaratmazsın.
