<!--
Her projede geçerli çekirdek ilkeler. Bu dosya projeye KOPYALANMAZ: denetçi
bunu okur, üstüne referans incelemesinden ve kullanıcıdan geleni ekler,
projenin anayasasını `/speckit-constitution` prompt'u olarak verir. Dosyayı
komut yazar; sürüm ve tarih alanlarını da o doldurur.

Çekirdek beş ilkedir. Projeye özel ilke en çok iki tane eklenir; toplam yediyi
geçmez. Anayasa araç ve rol adı taşımaz: ürünün kuralını söyler, kimin hangi
araçla çalıştığını değil. Mecburi teknoloji ve platform kısıtları ilkelere
değil "Ek Kısıtlar"a girer.
-->

# Anayasa

## Core Principles

### I. Davranış İddiası Ölçümsüz Kurulmaz

Bir aracın ya da ürünün performansı, sınırı, garantisi (dayanıklılık, tutarlılık,
izolasyon, güvenlik) ya da sürüme bağlı davranışı hakkındaki bir iddia ancak
ölçümle kabul edilir (MUST). Dokümandaki rakam ve modelin eğitim bilgisi bu
iddiayı taşımaz; hangi sürümün davranışı olduğu bilinmez.

İddiaya dayanan karar ölçümün özetini kendi gerekçesinde yazar: ne ölçüldü, hangi
sürüm ve ortamda, sonuç ne, nasıl yeniden koşulur (MUST). Dış bir kayda bağlantı
eklenebilir ama tek kanıt o olamaz; ürünün belgeleri kendi kendine yetmelidir.

Ölçülemiyorsa iddia kurulmaz; ölçüm borcu yazılır ve iddiaya dayanan iş "tamam"
sayılmaz (MUST).

Teknoloji seçimi bu ilkeye değil İlke V'e tabidir. Seçimin gerekçesi bir davranış
iddiasına dayanıyorsa yalnız o iddia buraya girer.

Gerekçe: Belgelenen davranış ile gözlenen davranış ayrışır, kararı yalnız gözlenen
taşır. Ürün belgesinde durmayan kanıt, belgeyi okuyan için yoktur; yazılmayan
ölçüm bir sonraki soruda yeniden sorulur.

### II. Kanıt Ölçtüğü Şeyin İçinden Çıkmaz

Ölçen kod ürün kodunu import etmez ve ürünün durumunu değiştirmez (MUST NOT).
Doğrulayan taraf doğrulanan taraf olamaz.

Bundan üç ayrım doğar ve bir dosyanın hangisi olduğu bulunduğu dizinden
anlaşılır: üretimde koşan kod, kurulumu bir kez yapan kod, ölçen kod.

Test kanıt değildir: birim test kodun kendi doğruluğunu sınar; kanıt kapısı
ürünün dış dünyaya verdiği sözü sınar ve negatif kontrolü olmalıdır (MUST).

Gerekçe: Ürün kodu değiştiğinde kanıtın da değişmesi, kanıtı ürünün bir görüşüne
çevirir.

### III. Tek Kaynak Spec

Üretilen artefaktların tek kaynağı spec'tir. Ön çalışma belgeleri, tasarım
notları ve özellik listeleri spec'in girdisidir; spec yazıldıktan sonra kaynak
değildir. Hiçbir kontrol onlara sormaz, hiçbir artefakt onlara atıf yapmaz
(MUST NOT).

Bir kararın gerekçesi spec'te yoksa yoktur; başka bir belgede olabileceği
varsayılamaz. Spec ve plan, girdilerinin taşıdığı bilgiyi aşmalıdır (MUST):
aşmıyorsa ya girdinin yarısı çöptü ya spec eksik yazıldı, ikisi de kayıttır.

Gerekçe: İki kaynak arasında senkron tutmak, tek kaynak ile kod arasında senkron
tutmaktan pahalıdır; üçüncü kaynak onu imkânsız yapar.

### IV. Önce Sadelik

Problemi çözen en az bileşen seçilir. Olgun bir çözümün yaptığı iş yeniden
yazılmaz. Spekülatif esneklik, yapılandırılabilirlik ya da "ileride lazım olur"
bileşeni eklenmez (MUST NOT). Eklenen her bileşen, hangi somut gereksinimi
karşıladığıyla gerekçelendirilmelidir (MUST).

Koşmayan bir dosya ağaçta durmaz. "Sonra düzeltiriz" diye tutulan bir kontrol
hiçbir şey ölçmeden kırmızı yanar ve ölçen bir kontrolün kırmızısını
değersizleştirir. Yazılmamış olanın gerekçesi metinde durur, kodda değil.

Gerekçe: Her ek bileşen işletme, güvenlik ve arıza yüzeyi maliyetidir.

### V. Kanıtlanmış Yaklaşım Yeniden Keşfedilmez

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
  doldurulur, teknik terimler çevrilmez. Kod ve commit mesajları İngilizcedir.

<!-- Projeye özel kısıtlar buraya: mecburi platform, mecburi teknoloji,
     uyumluluk ve operasyon kısıtları. İlkelere teknoloji adı girmez. -->

## Geliştirme Akışı ve Kalite Kapıları

- Her spec, plan ve task ilgili olduğu ilkelere geri izlenebilir olmalıdır
  (MUST); hiçbir ilkeye bağlanamayan iş kapsam dışıdır.
- Ölçülmemiş adımların listesi, ölçülmüş sonuçlar kadar bir artefakttır ve bu
  listede olmayan hiçbir şey varsayım değildir. Her madde ne bilinmediğini ve
  neden önemli olduğunu yazar.
- "Yazıldı ama ölçülmedi" ayrı bir hâldir: kod derleniyor, birim testi var, ama
  gerçek ortamda hiç koşmadıysa o iş tamamlanmamıştır. Bir işaret kutusu bunu
  gösteremez.

## Governance

- Bu anayasa projedeki diğer tüm pratik ve alışkanlıkların üzerindedir; çelişki
  hâlinde anayasa kazanır.
- **Değişiklik usulü**: Öneri, hangi ilkeyi neden değiştirdiğini ve etkilediği
  mevcut kararları yazılı olarak belirtir. Proje sahibi onaylamadan hiçbir ilke
  eklenemez, değiştirilemez, kaldırılamaz.
- **Çekirdek**: I–V ortaktır; projeye özel ilkeler VI'dan itibaren ve en çok iki
  tane eklenir. Çekirdekte yapılan değişiklik yalnız bu projede kalır; başka
  projelerde de geçerli olması isteniyorsa çekirdeğin kendisine taşınmalıdır.
- **Sürümleme**: Semantic versioning. MAJOR = geri uyumsuz ilke kaldırma ya da
  yeniden tanımlama; MINOR = yeni ilke ya da bölüm; PATCH = ifade düzeltmesi.
- **Uyum denetimi**: Her spec, plan ve task incelemesinde anayasa uyumu kontrol
  edilir. Sapma ya reddedilir ya da gerekçesi ve süresi yazılı bir istisna
  olarak kaydedilir; plan'da gerekçeli sapma Complexity Tracking tablosuna
  yazılır. Sessiz sapma kabul edilmez.

<!-- Çekirdek sürümü: 2.0.0 (2026-09-16). Projenin anayasasındaki sürüm ve
     tarih satırını komut kendi şablonuna göre yazar. -->
