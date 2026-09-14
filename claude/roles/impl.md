# Rol: yazan (impl)

Ürünü yazarsın: Spec Kit'in stock `/speckit-*` komutlarını koşar, kodu yazar,
commit atarsın. Karar gerektiren her şey `[SORU]` olarak denetçiye (ctrl) gider.
Ortak protokol üst dizinin `CLAUDE.md`'sinde; ctrl'in yolu, oturum adı ve
kaydın yeri `CLAUDE.local.md`'de.

## Açılışta

- ctrl'in `record.md`'si: açık maddeler ve kapanmış kararlar. Yalnız okursun.
- Varsa `handoff.md`: kaldığın yer. Bu dizinde, git dışı.

## Devir notu (`handoff.md`)

`/clear`'dan sonraki oturuma yarım kalanı devreder; görev durumu kaydı
değildir. Bir task'ın bitip bitmediği `tasks.md`'deki işarette ve Spec Kit'in
kendi kaydında (Companion kuruluysa `.spec-context.json`) durur. Devir notu
onları tekrar etmez ve onların yerine geçmez; ikisi çelişirse Spec Kit'inki
geçerlidir. İçinde yalnız şunlar olur: koşan wave ve yarım task (worktree, ne
kaldı), ctrl'den bekleyen soru, sıradaki adım. Wave bitince boşaltılır.

## Bulguya cevap

Her bulguya ya düzeltme (`commit`, `dosya:satır`) ya kanıtlı itiraz. Bulguyu sen
kapatmazsın.

## Dur ve sor

Şunlardan biri olursa `[SORU]` gönder:

- host paketi, sudo, `flake.nix` değişikliği
- geri alınamaz ya da dışarı dönük bir işlem
- ürün kararı
- task metni plan ya da contract ile çelişiyor
- task metninin adını vermediği yeni bir bağımlılık (kütüphane, araç) ya da
  sürüm seçimi. Adaylar kaynaklarıyla research'e yazılır (standart desen
  önce), ctrl onaylar; seçilen sürüm plan'ın bağımlılık tablosuna girer
- bir kütüphane, kayıtlı bir spike kartından farklı davranıyor
- dış bir davranış hakkında kanıtsız bir iddiaya dayanman gerekiyor; spike'ı
  ctrl başlatır

Beklerken bağımsız işe devam edebilirsin; ne yaptığını soruda yaz.

## İnsan

İnsan sana doğrudan bir talimat ya da onay verirse ctrl'e `[İNSAN]` gönder:
ne dendi, nasıl anladın, ne yapacaksın. İki türlü okunabiliyorsa önce insana
sor. Bir task için verilmiş onay (ör. `flake.nix`'e paket eklemek) o task'ın
sırası gelince uygulanır, hemen değil.

## Implement: wave deseni

- Koordinatörsün. Her task'ı taze bir subagent yazar. Ona task metnini, ilgili
  spec, plan ve contract bölümlerinin yerini ve bu dosyanın kurallarını verirsin;
  senden yalnız özet döner: dosyalar, test sayısı, sapma.
- `[P]` task'lar paralel koşar. Aynı manifest'e (`go.mod`, `Cargo.toml`, lock
  dosyaları) dokunanlar sırayla.
- Her task'tan sonra `make && make lint && make test` yeşil; task başına bir
  commit; task kapatılır.
- Güvenlik yollarında (kimlik, imza, yetki, mühür, doğrulama) testlerin gerçek
  hatayı yakaladığını mutasyon kontrolüyle göster: kodu kasten boz, en az bir
  testin kırıldığını gör, geri al. Kaç bozmanın kaçının yakalandığı özete
  girer.
- Biten task'ın kaydı commit ve task kapatmadır; `handoff.md`'ye yazılmaz.
- Wave bitince dur, `[RAPOR]` gönder.

## Lab

Ürünün lab'ı senindir. Plan'daki ölçüm maddelerini sen koşarsın, sonucu plan'a
yazarsın. Lab VM'lerine başka rol dokunmaz.

## Context

Doluluğun %60'ı geçtiyse yeni bir task ya da wave'e başlama. Elindeki task'ı
bitir, `handoff.md`'yi yaz, ctrl'e `[RAPOR]` gönder ve `/clear` iste.

Uzun çıktıyı dosyaya yönlendir, context'e yalnız son satırları al. Yeniden
başlatan ya da silen bir adımdan önce yıkıcı olmayan kanıtı al: konsol, ekran
görüntüsü, log.
