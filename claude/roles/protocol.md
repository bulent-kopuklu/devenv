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
`/speckit-constitution` (projenin bütün işini bağlayan kurallar),
`/speckit-specify` (ürünün ne yapacağı), `/speckit-clarify` (spec'teki
belirsizlikleri soru-cevapla kapatır), `/speckit-plan` (nasıl yapılacağı),
`/speckit-tasks` (fazlara bölünmüş iş listesi), `/speckit-analyze` (belgeler
arası tutarsızlık raporu) ve `/speckit-companion-implement` (bir fazın kodunu
yazar). Bir komutun ne yaptığı impl'de `.claude/skills/<komut>/SKILL.md`
dosyasında yazar.

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
