---
name: reference
description: Referans ürün araştırması. Bu işi yapan ürünleri linkleriyle listeler, insan seçer; sonra her soru için (bir özellik, bir karar, takılınan bir yer) seçilen ürünlerin bunu nasıl çözdüğünü dokümanlarından, forumlarından ve kaynak kodundan bulur. Özellik listesi çıkarılırken ve impl'in bir sorusu referansta cevap ararken yüklenir.
---

# Referans araştırması

Çıktın bu dizinde: `reference/<ürün>.md`. Wiki'ye yazmazsın; wiki yalnız spike
içindir. Ajan açmazsın: aramayı ve okumayı kendin yaparsın.

Başlamadan önce ne yapılacağı, kimin için yapılacağı ve mecburi kısıtlar belli
olmalı. Belli değilse insana sorarsın; belliyse sormazsın.

## 1. Tarama

Referans ürünler seçilmediyse bu işi yapan ürünleri web'de ararsın. İnsana
liste sunarsın: ad, tek satırlık tanıtım, link. Analiz yok, rakam yok. İnsan
referans ürünleri seçer.

## 2. Soruya göre araştırma

Her araştırma bir sorudan başlar: bir özellik, bir karar ya da takılınan bir
yer. Önce `reference/<ürün>.md`'de cevap var mı bakarsın. Yoksa seçilen her
ürünün bunu nasıl çözdüğünü ararsın: dokümanında, forumlarında (issue,
tartışma), ürün açık kaynaksa kodunda.

Bulguyu `reference/<ürün>.md`'ye eklersin: soru; ürünün davranışı ya da
çözümü; kaynağı (link, dosya, sürüm). Dosyanın başında ürün, sürüm ve inceleme
tarihi durur.

- Kaynağı olmayan cümle bulgu değildir, yazılmaz.
- Rakam uydurulmaz.
- Bulamadıysan "bulunamadı" ve nerelere baktığını yazarsın; okuyan "üründe
  yok" ile "bakılmamış"ı ayırt edebilsin.
