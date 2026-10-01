# {{NAME}} Anayasası


## Core Principles

### I. Davranış İddiası Ölçümsüz Kurulmaz

Bir aracın ya da ürünün performansı, sınırı, garantisi (dayanıklılık, tutarlılık,
izolasyon, güvenlik) ya da sürüme bağlı davranışı hakkındaki bir iddia ancak
ölçümle kabul edilir (MUST). Dokümandaki rakam ve modelin eğitim bilgisi bu
iddiayı taşımaz; hangi sürümün davranışı olduğu bilinmez.

İddiaya dayanan karar ölçümün özetini kendi gerekçesinde yazar: ne ölçüldü, hangi
sürüm ve ortamda, sonuç ne, nasıl yeniden koşulur (MUST). Dış bir kayda bağlantı
eklenebilir ama tek kanıt o olamaz; ürünün belgeleri kendi kendine yetmelidir.

Ölçülemiyorsa iddia kurulmaz (MUST).

Teknoloji seçimi bu ilkeye değil İlke V'e tabidir. Seçimin gerekçesi bir davranış
iddiasına dayanıyorsa yalnız o iddia buraya girer.

Gerekçe: Belgelenen davranış ile gözlenen davranış ayrışır, kararı yalnız gözlenen
taşır. Ürün belgesinde durmayan kanıt, belgeyi okuyan için yoktur; yazılmayan
ölçüm bir sonraki soruda yeniden sorulur.

### II. Tek Kaynak Spec

Üretilen artefaktların tek kaynağı spec'tir. Ön çalışma belgeleri, tasarım
notları ve özellik listeleri spec'in girdisidir; spec yazıldıktan sonra kaynak
değildir. Spec yazılınca girdiyi eksiksiz taşıdığı bir kez karşılaştırılır;
sonrasında hiçbir artefakt girdiye atıf yapmaz (MUST NOT).

Bir kararın gerekçesi spec'te yoksa yoktur; başka bir belgede olabileceği
varsayılamaz.

Gerekçe: İki kaynak arasında senkron tutmak, tek kaynak ile kod arasında senkron
tutmaktan pahalıdır; üçüncü kaynak onu imkânsız yapar.

### III. Önce Sadelik

Problemi çözen en az bileşen seçilir. Olgun bir çözümün yaptığı iş yeniden
yazılmaz. Spekülatif esneklik, yapılandırılabilirlik ya da "ileride lazım olur"
bileşeni eklenmez (MUST NOT). Eklenen her bileşen, hangi somut gereksinimi
karşıladığıyla gerekçelendirilmelidir (MUST).

Koşmayan bir dosya ağaçta durmaz. "Sonra düzeltiriz" diye tutulan bir kontrol
hiçbir şey ölçmeden kırmızı yanar ve ölçen bir kontrolün kırmızısını
değersizleştirir. Yazılmamış olanın gerekçesi metinde durur, kodda değil.

Gerekçe: Her ek bileşen işletme, güvenlik ve arıza yüzeyi maliyetidir.

### IV. Kanıtlanmış Yaklaşım Yeniden Keşfedilmez

Bir tasarım kararından önce — mimari, protokol, veri modeli, algoritma, operasyon
akışı — aynı problemi çözmüş ve üretimde kendini kanıtlamış çözümler incelenir
(MUST): yaygın açık kaynak projeler, standartlar, olgun ürünler. Girdi bir
referans verdiyse inceleme ondan başlar.

Örnek, problemin bağlamını paylaşan çözümler arasından seçilir; bağlamı farklı
bir örnek, farkı yazılmadan dayanak sayılmaz. Örnekte ne yapıldığı modelin
hafızasından değil kaynağından okunur ve her karar kaynağıyla (repo, dosya,
doküman, sürüm) yazılır. Gerekçesiz sapma kabul edilmez.

Örnek, yaklaşımın kaynağıdır, davranışının kanıtı değildir: hız, dayanıklılık ve
ölçek iddiaları İlke I'e tabidir.

Seçilen her dış bileşenin lisansı kontrol edilir ve kararın gerekçesinde
yazılır (MUST). Ürüne girdiğinde sorun çıkarabilecek bir lisans — güçlü copyleft
(GPL, AGPL), kaynağı açık ama kullanımı kısıtlı lisanslar (SSPL, BUSL, Elastic
License), ticari kullanımı yasaklayan ya da lisansı belirsiz bileşen — açıkça
uyarı olarak yazılır (MUST).

Güvenlikte istisna yoktur ve ölçü daha serttir. Standart desen aranır: RFC ya da
yayımlanmış bir standart, yaygın ve bakımlı bir kütüphane, bilinen bir protokol.
Kripto primitifi ve protokol kendimiz yazılmaz (MUST NOT). Özel çözüm ancak
adaylar incelenip neden yetmediği kaynakla yazıldıktan sonra tasarlanır.
Kaynağı olmayan güvenlik kararı kabul edilmez (MUST NOT).

Gerekçe: Üretimde yıllarca sınanmış bir çözüm, sıfırdan bulunan yaklaşımın henüz
karşılaşmadığı arızaları çoktan görmüştür; onu yeniden keşfetmek aynı arızaları
sırayla yeniden yaşamaktır. Güvenlikte bu daha ağır basar, çünkü güvenlik
mekanizmasının hatası işlevsel testte görünmez, ancak biri onu kırmaya
çalıştığında ortaya çıkar.

## Ek Kısıtlar

- Üretilen doküman ve çıktı dosyaları (spec, plan, araştırma notu, task listesi,
  checklist) Türkçe yazılır (MUST). Şablon İngilizce olsa bile içerik Türkçe
  doldurulur. Şablonun başlıkları, kimlik biçimleri ve anahtar kelimeleri içerik
  değildir; olduğu gibi kalır. Teknik terimler çevrilmez. Kod ve commit mesajları
  İngilizcedir.

## Governance

- Bu anayasa projedeki diğer tüm pratik ve alışkanlıkların üzerindedir; çelişki
  hâlinde anayasa kazanır.
- **Değişiklik usulü**: Öneri, hangi ilkeyi neden değiştirdiğini ve etkilediği
  mevcut kararları yazılı olarak belirtir. Proje sahibi onaylamadan hiçbir ilke
  eklenemez, değiştirilemez, kaldırılamaz.
- **Kapsam**: Anayasa ürünün gereksinimini ve teknoloji kararını taşımaz:
  gereksinim spec'e, teknoloji kararı plan'ın girdisine gider. Bu metin her
  projede ortaktır; bir projede yapılan değişiklik yalnız o projede kalır, başka
  projelerde de geçerli olması isteniyorsa ortak metne taşınır.
- **Sürümleme**: Semantic versioning. MAJOR = geri uyumsuz ilke kaldırma ya da
  yeniden tanımlama; MINOR = yeni ilke ya da bölüm; PATCH = ifade düzeltmesi.
- **Uyum denetimi**: Her spec, plan ve task incelemesinde anayasa uyumu kontrol
  edilir. Sapma ya reddedilir ya da gerekçesi ve süresi yazılı bir istisna
  olarak kaydedilir. Sessiz sapma kabul edilmez.


**Version**: 1.0.0 | **Ratified**: {{DATE}} | **Last Amended**: {{DATE}}
