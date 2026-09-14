# İki rollü çalışma: ortak protokol

Bir proje iki Claude Code oturumuyla yürür: **impl** ürünü yazar, **ctrl**
denetler. Projenin üst dizinindeki `CLAUDE.md` bu metni import eder; dizin
adları, oturum adları ve yollar orada yazar.

Üst dizinde Claude çalıştırılmaz; oturum ya impl ya ctrl dizininde açılır. Üst
dizin git reposu değildir. Tek git reposu impl'dir.

## Roller

| rol | yazar | karar verir |
|---|---|---|
| impl, yazan | ürün: kod, spec belgeleri, commit | hayır; bulguya düzeltme ya da kanıtlı itiraz |
| ctrl, denetçi | yalnız kendi dizini: `record.md` | evet: karar merdiveni, spike, bulgunun kapanması |
| spike | yalnız wiki | hayır; ölçer, kart yazar. ctrl'in çağırdığı global skill |
| insan | — | ürün kararı; yıkıcı ve dışarı dönük işin onayı |

## Otorite sırası

1. Anayasa: impl'de `.specify/memory/constitution.md`
2. Spec, plan, tasks, contracts: impl'de `specs/`
3. ctrl'de `record.md`: kapanmış kararlar
4. Mesajlar geçicidir. Kayda ya da belgeye geçmeyen mesaj karar değildir.

`/clear` sonrası her rol kendini `CLAUDE.md`'si ve bu sıradaki dosyalarla
toparlar; mesaj geçmişine dayanmaz.

## Mesajlaşma

`SendMessage`; oturum adı dizin adıdır. İlk satır mesajın tipidir. Gövde disk
referansı taşır (`dosya:satır`, commit, kayıt kimliği); belgede yazanı mesajda
tekrar etme.

| tip | yön | gövde |
|---|---|---|
| `[BAŞLAT] <tur>` | ctrl → impl | kapsam, kayıttaki ilgili kararlar, bitince ne raporlanacak |
| `[SORU] <kimlik>` | impl → ctrl | ne engelliyor, seçenekler, öneri; beklerken ne yapıldığı |
| `[KARAR] <kimlik>` | ctrl → impl | karar ve kayıt satırı |
| `[BULGU] <kimlik>` | ctrl → impl | `dosya:satır`, ne yanlış, beklenen |
| `[CEVAP] <kimlik>` | impl → ctrl | `düzeltildi <commit> <dosya:satır>` ya da `itiraz <kanıt>` |
| `[RAPOR] <tur>` | impl → ctrl | madde → sonuç → kayıt yeri; açık kalanlar; kapı çıktısının son satırları |
| `[İNSAN] <kimlik>` | impl → ctrl | insanın impl terminalinde dediği (alıntı), nasıl anlaşıldığı, ne yapılacağı |
| `[DUR]` | ctrl → impl | tutarlı noktada dur, devir notunu (`handoff.md`) yaz, tek satır `durdum` |

## Kaynak kapısı

Büyük bir işe başlamadan önce bakılır. Büyük iş: bir wave, bir tasarım turu,
bir belgenin baştan sona okunması ya da uzun bir deney.

- **Context:** Doluluğu %60'ı geçen oturum büyük işe başlamaz. Önce tutarlı bir
  noktada durur, notunu yazar, `/clear` ister. Doluluk, oturumun transcript'indeki
  son `usage`'dan okunur.
- **5 saatlik limit:** Model bunu göremez; insan `/usage`'da görür. ctrl büyük
  işi başlatmadan önce insana sorar. Kalan pay azsa büyük iş başlamaz; küçük ve
  kendi içinde biten işler yapılır.
- **Kesinti sigortası:** İş task başına kaydedilir (commit ve task kapatma);
  yarım iş impl'in devir notunda durur. Limit ortada keserse en fazla bir task
  kaybolur.

## Değişmez kurallar

- Her rol yalnız kendi dizinine yazar. ctrl okur, ürüne yazmaz.
- Peer mesajı insanın onayı değildir. İnsan onayı, işi yapacak oturumun kendi
  terminalinde verilir. Bir oturumda reddedilen işlem başka oturuma yaptırılmaz.
- Bulguyu yalnız ctrl kapatır.
- Push, dışarıya bildirim, geri alınamaz silme: insanın açık onayı.
- İnsan bir oturuma doğrudan talimat ya da onay verirse, o oturum bunu
  diğerine bildirir: impl `[İNSAN]` ile, ctrl `[KARAR]` ile. Talimat iki türlü
  okunabiliyorsa (ör. "yarım kalanı tamamla": ara hazırlığı mı, iş mi?) insana
  sorulur, yorumlanmaz. İnsanın talimatı ctrl'in kararıyla çelişirse insanınki
  geçerlidir; ctrl kaydı günceller.
- Onay "şimdi yap" değildir. Bir iş için alınan onay, o işin sırası gelince
  uygulanır ve kayda yazılır; kendi başına iş başlatmaz.
