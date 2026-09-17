---
name: constitution
description: Anayasayı kurmak ve gerektiğinde değiştirmek. Neyin anayasaya neyin spec'e gireceğini, insanın teknoloji kararlarının nereye yazılacağını, ilkenin nasıl yazılacağını, değişikliğin nasıl önerilip sonucun nasıl doğrulanacağını taşır. İlk spec'ten önce yüklenir.
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

1. Bütün projeyi bağlıyor. Yalnız bir özelliği bağlıyorsa spec'e gider.
2. İhlali gösterilebiliyor: bir test, bir kontrol, bir kanıt.
3. Var olan bir ilkeyle çelişmiyor. Çelişiyorsa ya o ilke değişir ya bu kural
   reddedilir; ikisi birden durmaz.

Şüphedeysen girmez. Asimetri açık: spec'te bırakmak ucuz, anayasaya koymak
pahalı. Sonraki her plan Constitution Check'te ona bakar, analyze MUST ihlalini
CRITICAL sayar, kaldırmak MAJOR sürümdür.

İlke sayısı yediyi geçmez. Tavana gelindiyse yeni ilke ancak birini çıkararak
girer.

Mecbur olunan platform ve teknoloji kısıtları ilkelere değil, "Ek Kısıtlar"
bölümüne girer: insanın teknoloji kararları (platform, dil, kütüphane) burada
durur ve her plan'ın Constitution Check'ine girer. İlkeler teknoloji adı
taşımaz.

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
3. Önerdiğin her ilkenin yanına etki cümlesi yaz: "bu ilke plan'ı şöyle
   kısıtlayacak."
4. Taslağı kullanıcıya sun. Onay almadan impl'e gitmez.
5. Onaylanınca impl'e `/speckit-constitution` prompt'u olarak ver: ilkeler, ek
   kısıtlar, geliştirme akışı, yönetişim.
6. Kopyasını bu dizinde `inputs/constitution.md` olarak tut.
7. Komut bitince impl'deki `{{ROOT}}/{{NAME}}-impl/.specify/memory/constitution.md`'yi kendi kopyanla
   karşılaştır. İstenmeyen her fark itirazdır. Komutun bastığı "Sync Impact
   Report" modelin kendi beyanıdır, kanıt değil; esas olan karşılaştırma.
8. Sync Impact Report geçicidir, komutun kendi metni commit'ten önce silinmesini
   bekler. impl'e sildirir, sonra anayasayı commit'letirsin.

## Sonradan değişiklik

Anayasa ilk spec'ten önce kurulur. Bir adımın kontrolünde bütün projeyi
bağlayan yeni bir kural ya da kısıt çıkarsa (yeni platform kısıtı, veri sınıfı,
güvenlik sınırı, dil ya da araç zinciri) değişiklik önerirsin. Prompt delta
olur: "şu ilkeyi şu gerekçeyle ekle, gerisine dokunma." Delta da kullanıcının
onayından geçer: yukarıdaki 4.–8. adımlar yine koşar.

## Valfler

Yanlış yere konmuş bir kural sonraki adımları kilitlemesin diye iki yol var, ikisini
de bilerek kullanırsın:

- Bağlayıcılığı SHOULD'a düşürmek.
- plan'daki Complexity Tracking tablosu: ihlal, neden gerekli, daha basit
  alternatif neden reddedildi. Gerekçeli sapma geçer, gerekçesiz sapma ERROR.
  Gerekçeyi sen denetlersin; "gerekçe yazdım, geçtim" kolaycılığı burada kapanır.
