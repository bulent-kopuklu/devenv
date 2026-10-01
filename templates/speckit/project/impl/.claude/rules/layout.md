# Yerleşim ve test

DIKKAT: Asagida anlatilan yerlesim plani, `speckit-plan` da mumkun oldugunca uygulanmalidir. 
Esnetilmek istenilen kurallar icin ctrl vasitasiyla insandan onay alinir.

Bu dosya dilden bağımsızdır. Bir dilin kaynağı nereye koyduğu
`.claude/rules/<dil>.md`'nin Yerleşim bölümünde, nasıl derlediği
`makefile.md`'de; testleri nereye koyduğu ve `tests/`'i teslimden nasıl
ayırdığı `.claude/rules/<dil>-testing.md`'dedir.

## Yerleşim

- Ürün kodu yalnız `components/<ad>/` altında, ürünü dışarıdan ölçen kod
  yalnız `evidence/` altında durur. Bir bileşenin ürün kodu (teslim
  edilen kütüphane ya da binary) tek dildir. Başka bir dilde bileşen
  gerekiyorsa plan'da yazılır ve proje sahibine sorulur.
- Bileşen dizini bileşenin köküdür: kendi `Makefile`'ı, manifest'i (`go.mod`,
  `Cargo.toml` gibi), kaynağı ve `tests/`'i orada durur. Kaynağın yeri dilin
  alışkanlığıdır; dilin kural dosyası yazar.
- `tests/` bileşenin içindedir ama teslimin parçası değildir: derlenen,
  dağıtılan ya da yayımlanan pakete girmez.
- evidence ürünü dışarıdan, bir kullanıcı gibi ölçer; neyi sınadığı
  `testing.md`'nin Evidence bölümündedir. Bileşenin değil sistemin testidir;
  kökteki `evidence/`'dadır:

  ```
  evidence/
  ├── Makefile
  ├── pyproject.toml, uv.lock  script'lerin manifest'i
  ├── sysenv/                  ortam düzeneği; kendi Makefile'ı
  ├── <bileşen>/               yalnız bu bileşeni kullanan senaryolar
  │   ├── Makefile
  │   ├── disasters.md         felaket tablosu ve senaryo listesi
  │   ├── probes/<ad>/         probe'lar
  │   ├── <NN_katman>/         senaryolar
  │   ├── setup/               bu bileşene özgü kurulum (şema, seed)
  │   └── check/               denetçiler
  └── systems/<ad>/            birden çok bileşeni kullanan senaryolar
      ├── Makefile
      └── disasters.md         felaket tablosu ve senaryo listesi
  ```
- Probe ürünü bir kullanıcı gibi kullanan bir binary'dir (command gönderen,
  event yazan, saga ve handler koşan kod). Ürünün dilinde yazılır, yalnız
  ürünün public API'sini kullanır ve gördüğünü kaydeder. API'sini kullandığı
  bileşenin `probes/`'undadır; ortak kodu da oradadır. Adı ürünün hangi kullanımını taklit ettiğini söyler
  (`saga-timeout`, `projection-local`); genel bir ad (`service`, `app`,
  `worker`) ya da senaryonun adını almaz. Bir probe'u birçok senaryo
  kullanabilir, bir probe tek bir senaryo için de yazılabilir. Probe'u yalnız
  evidence kullanır; acceptance testi ve sistem senaryosu probe kullanmaz,
  birden çok instance'ı kendisi başlatır.
- Probe ile parametre arasındaki sınır: gerçek bir kullanıcı farkı kodla
  yapıyorsa ayrı probe'dur; config'le ya da dağıtımla yapıyorsa (ürünün
  ayarları, yükün ölçeği, arızanın hedefi) parametredir. Sınama sorusu: değer
  değişince probe'un adı yalan olur mu?
- Tek bileşeni kullanan senaryo `evidence/<bileşen>/`'dedir; birden çoğunu
  kullanan `evidence/systems/<ad>/`'dedir. Sistem bir deployable bileşimidir;
  adı bir bileşenin adı olamaz; onu getiren plan adlandırır, sonraki plan'lar yoluyla anar. Sistem
  probe'ları kopyalamaz, bileşenin dizininden derletir. Yön tektir: sistem
  bileşenin evidence'ını kullanır; bileşen evidence'ı kullanmaz.
- Bileşenden bağımsız olan her şey `sysenv/`'dedir: container ve ağ kurmak,
  ağı yavaşlatmak, CPU ve belleği sınırlamak, microVM, arıza sokmak, çıktıyı
  yazmak. `sysenv/` hiçbir bileşenin adını ya da anlamını bilmez;
  `evidence/<bileşen>/setup/` yalnız o bileşene özgü kurulumu taşır.
- Bir insanın eliyle ve gözüyle yapacağı her şey script'tir: ortamı kurmak
  (container, ağ, şema), probe'ları başlatıp durdurmak, arıza sokmak (kill,
  durdurma, ağ kesme, gecikme), veritabanına ve broker'a bakmak, saymak, hüküm
  vermek, rapor yazmak. Script'ler `evidence/` altında, kendi
  manifest'iyle durur. Tercihimiz Python'dur; Burada kullanilan python 
  development icin degildir o yuzden bağımlılıkları uv ile `pyproject.toml` ve 
  `uv.lock`'ta durur (uv devshell'den gelir, paketler flake'e girmez). 
  Bir satırlık iş bash'le yazılır. Başka bir dil seçilirse plan'da yazılır
  ve proje sahibine sorulur.
- Her senaryo, adı neyi sınadığını söyleyen bir script'tir; adı spec'in
  kimliğini taşımaz.
- Bir iş hem probe'a hem script'e yazılabiliyorsa script'e yazılır. Probe'a
  ancak ürünü çağırmadan yapılamıyorsa girer.
- Yeni bileşen `components/` altında yeni dizindir; plan'da yazılır ve proje
  sahibine sorulur.
- Kökte yalnız projenin geneline ait olan durur: `Makefile`, `flake.nix`,
  formatter/linter config'leri, editör ayarı `.vscode/`, `CLAUDE.md`, `README.md`, 
  `docs/`, `components/`, `evidence/`. Spec Kit kullanılıyorsa onun yerleri de: `specs/`, `.specify/`, living
  specs'in `living-specs.yml`'ı ve `capabilities/`'i. Kök dizine kaynak kodu ya
  da bunların dışında yeni dizin eklenmez.
- `docs/` yalnız insan içindir. Ajan oraya istendiğinde yazar ve düzenlerken
  okuyabilir. Ama `docs/` otorite değildir: oturum açılışında okunmaz; spec,
  plan, tasks ve kod ona dayanmaz ve referans vermez. `docs/` ile spec/plan
  çelişirse spec/plan esastır, `docs/` güncellenir.
- Bileşenler arası sözleşme (proto, OpenAPI) kendi bileşeninde durur
  (`components/<ad>/`, manifest `buf.yaml`). Kodunu onu kullanan her bileşen
  kendi build'inde üretir: Go `//go:generate`, Rust `build.rs`. Sözleşme
  bileşeni derlenmez.
- Bir bileşenin evidence dışındaki bütün testleri ve bench'i kendi
  dizinindedir; bileşen dizini kopyalanınca testleriyle taşınır. evidence
  bileşene değil sisteme aittir.

## Test

- Bu bölüm genel düzendir. Proje kendi ihtiyacına göre tür, katman, hedef ya
  da denetim ekleyip çıkarabilir; tür → yer → hedef mantığı değişmez. Eklenen
  her şey plan'da yazılır ve proje sahibine sorulur. Kodun yanında duran
  testlerin dosya adı, etiketi ve aracı dilin kural dosyasının Test
  bölümündedir.
- unit, acceptance, sistem senaryosu ve contract testlerinin türü ve yeri
  `testing.md`'dedir. evidence, bench ve probe'un yeri:

  | tür | yer |
  |---|---|
  | evidence | `evidence/<bileşen>/<NN_katman>/` ya da `evidence/systems/<ad>/`; script (Yerleşim) |
  | bench | `components/<ad>/tests/bench/` |
  | probe | `evidence/<bileşen>/probes/<ad>/`, her biri bir binary |
  | probe'ların ve script'lerin kendi testleri | test ettikleri kodun yanında, `evidence/` altında |

- spec-kit'in plan ve tasks şablonundaki adların karşılığı: `tests/unit`
  kodun yanındaki unit test, `tests/integration` acceptance, `tests/contract`
  contract. evidence'ın ve sistem senaryosunun spec-kit'te karşılığı yok.
- Her bench `tests/bench/` altındadır, tek bir fonksiyonu ölçen de; kodun
  yanında bench olmaz. bench ürünün uçtan uca özelliklerini tek process
  içinde kısa süre koşar; amacı sürümler arasındaki gerilemeyi görmektir.
  evidence'ın düzeneğini ve probe'larını kullanmaz.
- `NN_katman` dizinleri alttan üste numaralanır (10, 20, …); numara kodun
  katmanını söyler, spec'in kimliğini taşımaz. Ürün kodunda spec kimliği
  (FR, SC, T) geçmez; test kodu ürün kodu değildir.
- Probe teslim edildiği gibi, release bayraklarıyla derlenir: ölçülen,
  teslim edilen kütüphanedir.
- acceptance'ta ve sistem senaryosunda sabit bekleme yoktur; olay ya da
  işaret beklenir.
- Kapanış testi vardır: başlat, iş ver, iptal et; arkada çalışan hiçbir iş
  kalmadığını ve in-flight işin tamamlandığını doğrula.

## Evidence hazırlama

Evidence'ın referans dosyası her evidence
dizininin (`evidence/<bileşen>/`, `evidence/systems/<ad>/`) `disasters.md`'sinde
durur, senaryolarla birlikte commit'lenir ve spec'ten spec'e birikir. İki
bölümü vardır: felaket tablosu ve senaryo listesi. Her spec'in Evidence
hazırlaması ikisini de günceller: satır ekler, değiştirir ya da siler ve
nedenini yazar. Tabloda yeri olmayan bir senaryo atılmaz, listeye girer.
Tabloyu ve listeyi tek bir subagent'la çıkarırsın; birden fazla agent
kullanmazsın.

1. Tablonun satırları ürünün process rolleridir: sahada ayrı process olarak
   koşan her rol. Rolleri plan.md'nin yerleşiminden ve koddan çıkarırsın.
2. Tablonun sütunları felaketlerdir: process kill edilir; durdurulur
   (SIGSTOP); ötekilerden ayrı yavaşlar; process ile bir dış sistem
   arasındaki ağ kesilir (her dış sistem ayrı sütun).
3. Her hücreye o felakette ürünün tutması gereken sözü, spec'teki cümlesini
   aynen alıntılayarak yazarsın; spec merge'den sonra silindiği için kimliği
   (FR, SC) değil cümleyi taşırsın. Spec'te yoksa "spec'te yok" yazar, beklenen
   davranış için önerini eklersin. ctrl insana götürür; karar spec.md'ye
   yazılınca hücreyi o cümleye bağlarsın.
4. Her hücre şunlardan biridir: onu sınayan mevcut senaryo (yolu); yeni
   senaryo (adı, ölçtüğü söz, kullandığı probe'lar ve parametreleri); kapsam
   dışı ve gerekçesi (ör. rol o dış sisteme bağlanmıyor).
5. Listeye public API'yle oluşabilecek race condition'ları ve tabloya
   sığmayan öteki felaket senaryolarını yazarsın. Her madde neyin neyle
   yarıştığını ya da ne olduğunu, ürünün tutması gereken sözü (3'teki gibi)
   ve 4'teki durumlardan birini taşır.
6. Bu spec'te bulunan bug'lara bakarsın: her bug'ın ortaya çıktığı durum
   tabloda ya da listede bir senaryoyla sınanır.
7. `evidence/` altındaki her senaryoya bakarsın: sınadığı davranış kalktıysa
   silinir, değiştiyse güncellenir; tabloya ya da listeye nedeniyle yazılır.
8. Senaryonun ihtiyacına göre probe değişir ya da yenisi açılır; ayrım
   Yerleşim'deki probe ile parametre sınırıdır.
