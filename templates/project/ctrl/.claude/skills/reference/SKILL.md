---
name: reference
description: Referans ürün araştırması ve BL listesi. Ne yapacağımızı, kimin için yapacağımızı ve kısıtları konuşur; bu işi yapan ürünleri linkleriyle listeler; seçilen referansların bütün özelliklerini ve nasıl çalıştıklarını çıkarır; roadmap'i BL'lere böler. Sıfırdan bir projeye başlarken ya da referans incelemesi eksik kaldığında yüklenir.
---

# Referans araştırması

Çıktıların bu dizinde: `reference/<ürün>.md` ve `roadmap.md`. Wiki'ye yazmazsın;
wiki yalnız spike içindir. Ajan açmazsın: aramayı ve okumayı kendin yaparsın.

## 1. Görüşme

Üç şeyi öğrenirsin, tur başına en çok iki soru:

- Ne yapacağız?
- Kimin için? Kullanacak olan kim? "Bu iş yapılır mı, kime satılır" sorma;
  pazar ve müşteri analizi bu akışın işi değil.
- Mecbur olduğumuz platform, teknoloji ya da kısıt var mı?

Cevapları `roadmap.md`'nin başına yazarsın.

## 2. Tarama

Bu işi yapan ürünleri web'de ararsın. Kullanıcıya yalnız liste sunarsın: ad,
tek satır, link. Analiz yok, rakam yok. Kullanıcı bir, belki iki ürünü referans
seçer.

## 3. Çıkarım

Seçilen her ürün için `reference/<ürün>.md`. Bölümleri sırayla doldurursun; her
bölüm bitince kısa bir özet geçer, sonra devam edersin.

- **Kimlik:** ürün, sürüm, inceleme tarihi, kaynaklar.
- **Ne işe yarıyor:** bir paragraf.
- **Özellikler:** her biri için ne yaptığı, nasıl çalıştığı, kaynağı.
- **Nasıl çalışıyor:** bileşenler, akışlar, veri.
- **Güvenlik:** kimlik doğrulama, yetki, izolasyon, secret yönetimi, şifreleme,
  denetim izi. Bu bölüm atlanmaz.
- **Sınırlar:** ürünün yapmadıkları, bilinen kısıtları.
- **Kapsam tablosu:** başlık | incelendi · incelendi, üründe yok · incelenmedi |
  kaynak.
- **Yorum:** senin çıkarımların, bulgulardan ayrı, en sonda.

Kurallar:

- Her bulgu kaynağıyla yazılır. Kaynağı olmayan cümle yorumdur, Yorum bölümüne
  gider.
- Rakam uydurulmaz. Bulamadıysan "bilinmiyor" yazarsın.
- Ürün açık kaynaksa deposunu da okursun ve hangi dosyaya baktığını yazarsın.
- Kapsam tablosu şunun için var: dosyada bir özellik geçmiyorsa okuyan "üründe
  yok" mu, "bakılmamış" mı ayırt edemez.
- Sonradan bir soru için araştırma yaptıysan bulguyu bu dosyaya eklersin ve
  satıra "sonradan eklendi" yazarsın. Bu satırların birikmesi araştırmanın eksik
  kaldığının ölçüsüdür.

## 4. BL listesi

Özellikleri bağımlılığa göre gruplar, BL1'den başlayarak numaralandırırsın.

- Bir BL bir feature setidir, task değil. Ölçek örneği: "yedekten geri dönüş"
  bir BL'dir.
- Her BL bağımsız test edilebilir bir artış verir, önceliği bellidir ve
  öncekilere dayanır.
- Her BL için amaç, kapsam, kapsam dışı, bağımlılık, durum yazılır.
- Listeyi kullanıcıya sunarsın. Ekleme, çıkarma ve sıra değişikliğinden sonra
  `roadmap.md`'ye yazarsın.
- Yalnız sıradaki BL'nin spec'i hazırlanır. Sonrakilerin kapsamı plan ve
  araştırma sonucunda kayabilir; roadmap o zaman güncellenir.

## Bitince

Sıradaki iş anayasadır: `constitution` skill'i. Spec'e ondan sonra geçilir.
