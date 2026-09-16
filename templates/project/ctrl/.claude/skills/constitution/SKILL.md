---
name: constitution
description: Anayasayı kurmak ve her BL girişinde değişip değişmeyeceğine kurala göre karar vermek. Neyin anayasaya neyin spec'e gireceğini, ilkenin nasıl yazılacağını, değişikliğin nasıl önerilip sonucun nasıl doğrulanacağını taşır. İlk spec'ten önce ve her BL'ye geçerken yüklenir.
---

# Anayasa

Metni sen hazırlarsın, dosyayı impl'de `/speckit-constitution` yazar. impl'in
dosyasına sen yazmazsın.

Komutun ne yaptığını `{{ROOT}}/{{NAME}}-impl/.claude/skills/speckit-constitution/SKILL.md`'den,
şablonun şeklini `{{ROOT}}/{{NAME}}-impl/.specify/templates/constitution-template.md`'den
okursun. Aşağısı bugün kurulu sürümde doğrulandı; kurulu metin farklıysa o
esastır.

## Ne anayasaya girer

Bir kural ancak üçü birden doğruysa girer:

1. Bütün BL'leri bağlıyor. Yalnız bu BL'yi bağlıyorsa spec'e gider.
2. İhlali gösterilebiliyor: bir test, bir kontrol, bir kanıt.
3. Var olan bir ilkeyle çelişmiyor. Çelişiyorsa ya o ilke değişir ya bu kural
   reddedilir; ikisi birden durmaz.

Şüphedeysen girmez. Asimetri açık: spec'te bırakmak ucuz, anayasaya koymak
pahalı. Sonraki her plan Constitution Check'te ona bakar, analyze MUST ihlalini
CRITICAL sayar, kaldırmak MAJOR sürümdür.

Bir kural ilk göründüğü BL'de girmez. En az iki BL'de gerektiği görülünce ilke
adayı olur; tekrarı, önceki BL'lerin spec ve plan dosyalarından görürsün.

İlke sayısı yediyi geçmez. Tavana gelindiyse yeni ilke ancak birini çıkararak
girer.

Mecbur olunan platform ve teknoloji kısıtları ilkelere değil, "Ek Kısıtlar"
bölümüne girer. İlkeler teknoloji adı taşımaz.

Anayasa araç adı ve rol adı da taşımaz. "Şu skill'i koş", "denetçiye sor" gibi
bir cümle oraya girmez: anayasayı impl okuyor ve o araçlar onda yok, olmayan
bir aracın adını görünce kendi yorumunu uydurur. Kimin neyle çalıştığı rol
metinlerinde yazar.

Çekirdek beş ilkedir, projeye özel en çok iki ilke eklenir.

## İlke nasıl yazılır

- Beyan cümlesi, test edilebilir, muğlak dil yok.
- Bağlayıcılık kelimesi bilinçli seçilir: MUST ihlali analyze'da CRITICAL olur,
  SHOULD olmaz. Sert bağlamak istemediğin kuralı SHOULD yazarsın.
- İlke neyin zorunlu ya da yasak olduğunu söyler, nasıl yapılacağını değil.
- Her ilkenin sonunda gerekçesi durur.

## İlk kurulum

1. `{{CONFIG}}/constitution-base.md`'yi oku: her projede geçerli çekirdek.
2. Üstüne referans incelemesinden ve kullanıcıyla konuşmadan geleni ekle:
   platform kısıtları, veri kuralları, güvenlik kuralları.
3. Önerdiğin her ilkenin yanına etki cümlesi yaz: "bu ilke sıradaki BL'lerin
   planını şöyle kısıtlayacak."
4. Taslağı kullanıcıya sun. Onay almadan impl'e gitmez.
5. Onaylanınca impl'e `/speckit-constitution` prompt'u olarak ver: ilkeler, ek
   kısıtlar, geliştirme akışı, yönetişim.
6. Kopyasını bu dizinde `constitution.md` olarak tut.
7. Komut bitince impl'deki `{{ROOT}}/{{NAME}}-impl/.specify/memory/constitution.md`'yi kendi kopyanla
   karşılaştır. İstenmeyen her fark itirazdır. Komutun bastığı "Sync Impact
   Report" modelin kendi beyanıdır, kanıt değil; esas olan karşılaştırma.
8. Sync Impact Report geçicidir, komutun kendi metni commit'ten önce silinmesini
   bekler. impl'e sildirirsin.

## Her BL girişinde

Tetikleyici listesini işaretlersin. Hiçbiri işaretlenmezse karar "değişiklik
yok"tur.

- Bütün projeyi bağlayan yeni bir platform kısıtı ya da dış bağımlılık.
- Yeni bir veri sınıfı: kişisel veri, kimlik bilgisi, müşteri verisi. Saklama,
  şifreleme ve silme kuralı gerekir.
- Yeni bir güvenlik sınırı: yeni ağ yüzeyi, yeni kimlik doğrulama yolu, yeni
  yetki modeli.
- Yeni bir çalışma biçimi: sürekli çalışan servis, zamanlanmış iş, kuyruk. Hata
  ve çökme politikası gerekir.
- Yeni bir dil ya da araç zinciri: build, lint, test sözleşmesi değişir.
- Geri alınamaz bir işlem: silme, üzerine yazma, taşıma.
- Referans üründe görülen ve bütün projeye yayılması gereken bir kural.
- Önceki BL'de verilmiş bir karar bu BL'de de mecbur hâle geldi.

Değişiklik gerekmiyorsa yazacak bir şey yoktur; gerekiyorsa karar zaten
anayasanın kendisine giriyor.

Değişiklik gerekiyorsa prompt delta olur: "şu ilkeyi şu gerekçeyle ekle,
gerisine dokunma." Sonra yukarıdaki 7. ve 8. adımlar yine koşar.

Değişiklik ileriye dönüktür. Bitmiş BL'ler yeniden denetlenmez. Yeni ilke
onlarda bir ihlal yaratıyorsa bunu kayda yazar, düzeltme için ayrı bir BL
açarsın.

## Valfler

Yanlış yere konmuş bir kural sonraki BL'i kilitlemesin diye iki yol var, ikisini
de bilerek kullanırsın:

- Bağlayıcılığı SHOULD'a düşürmek.
- plan'daki Complexity Tracking tablosu: ihlal, neden gerekli, daha basit
  alternatif neden reddedildi. Gerekçeli sapma geçer, gerekçesiz sapma ERROR.
  Gerekçeyi sen denetlersin; "gerekçe yazdım, geçtim" kolaycılığı burada kapanır.
