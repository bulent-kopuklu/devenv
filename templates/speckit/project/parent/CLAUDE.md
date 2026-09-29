# {{NAME}}

# İki rollü proje

Bir yazılım ürünü iki Claude Code oturumuyla geliştirilir. Proje dizininde üç
dizin vardır; adları ve oturum adları bu metni yükleyen `CLAUDE.md`'de yazar:

- `<ad>/`: üst dizin. Git reposu değildir, burada oturum açılmaz.
- `<ad>-impl/`: ürünün git reposu. Burada **impl** oturumu çalışır: spec-kit
  komutlarını koşar; spec'i, planı, task'ları ve kodu yazar.
- `<ad>-ctrl/`: git reposu değildir. Burada **ctrl** oturumu çalışır: insanla
  konuşur, impl'e adımları sırayla yaptırır, her adımın çıktısını kontrol eder,
  impl'in sorularını cevaplar.

**İnsan** amacı, kısıtları ve ürün kararlarını verir; ctrl'le konuşur.

**spec-kit**, impl'in reposuna kurulu bir komut setidir. Komutlar sırayla:
`/speckit-specify` (ürünün ne yapacağı), `/speckit-clarify` (spec'teki
belirsizlikleri soru-cevapla kapatır), `/speckit-plan` (nasıl yapılacağı),
`/speckit-tasks` (fazlara bölünmüş iş listesi), `/speckit-analyze` (belgeler
arası tutarsızlık raporu), `/speckit-implement` (bir fazın kodunu yazar; ctrl
her fazı ayrı verir) ve `/speckit-converge` (kodun spec, plan ve tasks'a göre
eksiklerini `tasks.md`'ye yeni bir faz olarak ekler). Converge'den sonra
gereksiz kalan testler ayıklanır. Bütün testler en sonda `make gate` ile koşar; düşen test `/speckit-bug-assess`, `/speckit-bug-fix` ve
`/speckit-bug-test` ile kapanır. Bir komutun ne yaptığı impl'de
`.claude/skills/<komut>/SKILL.md` dosyasında yazar.

## Çalışma sırası

1. ctrl, impl'e bir komutu ve girdisini mesajla verir.
2. impl komutu koşar, bitince durur ve ctrl'e "bitti" der.
3. ctrl çıktıyı kontrol eder. İtirazı varsa impl'e yazar; impl düzeltir ve
   yeniden "bitti" der. impl katılmıyorsa gerekçesini yazar; anlaşamazlarsa
   ctrl konuyu insana götürür ve insanın kararını bekler.
4. İtiraz kalmayınca ctrl sıradaki komutu verir.

## Mesajlar

- Oturumlar `SendMessage` ile konuşur; alıcı, oturum adıdır.
- Mesaj düz yazıdır. Bir mesaj bir konu taşır; soru ya da itiraz mesajın ilk
  cümlesidir.

## Git

- İlk komuttan önce insan, impl'in reposunda remote'u ekler, dosyaları
  commit'ler ve `git push -u origin main` ile main'i bir kez gönderir.
- impl branch'lerde çalışır ve branch'i push eder. Bir branch'i main'e insan
  alır.


## Bu proje

| rol | dizin | oturum |
|---|---|---|
| impl | `{{NAME}}-impl/` | `cd {{NAME}}-impl && claude -n {{NAME}}-impl` |
| ctrl | `{{NAME}}-ctrl/` | `cd {{NAME}}-ctrl && claude -n {{NAME}}-ctrl` |
