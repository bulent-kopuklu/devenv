# Rust Kuralları

Bu dosya global geliştirme kurallarını Rust'a özgü olarak somutlaştırır.
Global kuralla çelişmez; onun Rust'taki karşılığını tanımlar.

## Modül Düzeni
- Tek dosyalık modüller için `mod.rs` KULLANMA, düz dosya kullan: `config.rs`, `error.rs`.
- Alt modülü olan modüller için `storage.rs` + `storage/` ikilisi (klasör adıyla aynı
  isimde dosya, `mod.rs` rolünü üstlenir).
- Yeni modül açarken bu kurala uy; `mod.rs` stiline geri dönme.

## Dayanıklılık (7/24 servis)
Hedef "hiç panic olmasın" değil — panik servisi DÜŞÜRMESİN, yayılmasın, sessizce yutulmasın.
- `unwrap()` / `expect()` / `panic!()` / `unreachable!()` / `todo!()` yerine hatayı
  `Result` ile döndür; çağıran karar versin.
- Array/slice indexleme yerine `.get()`; tamsayı taşmasında `checked_*` / `saturating_*`.
- Beklenen/geçici hatalar (ağ, I/O, parse) panik değildir — `Result` ile ele al,
  logla, gerekiyorsa retry/backoff uygula.
- Geri kazanılamayan invariant ihlali panik edebilir, ama:
  - spawn edilen her task panik'e karşı izole olmalı; `JoinHandle` sonucu kontrol edilmeli.
  - kritik task panic'inde supervisor yeniden başlatmalı, durumu loglamalı + metriğe yazmalı.
- `tokio` task'i sessizce ölmemeli: `JoinHandle` sonucunu yut(ma), logla.
- FFI / `cdylib` sınırında `extern "C"` fonksiyondan taşan panik süreci abort eder
  (Rust 1.81+); fonksiyonun gövdesini `std::panic::catch_unwind` ile sarmala.
- Her hata yolu yapılandırılmış log + metrik üretmeli. Sessiz hata yok.
- `expect()` yalnızca testte ve gerçekten imkânsız durumda kabul; test dışında gerekçe
  `#[expect(clippy::expect_used, reason = "…")]` içinde durur.
  ("İmkânsız sandığın için sessiz panic atma" — global "Önce Sadelik" kuralının Rust karşılığı.)

## Async Runtime
- Uygulama katmanında tek async runtime: **tokio**. Başka runtime (async-std vb.) ekleme.
- Yeniden kullanılabilir kütüphane crate'leri mümkünse runtime-agnostic kalsın
  (sadece `Future`/`Stream` döndür, runtime'a bağlanma).
- CPU-bound iş async task'ta çalıştırılmaz: `spawn_blocking` veya ayrı thread pool kullan.
- Bloklayan senkron çağrıyı (sync dosya I/O, sync DB driver) async context'te doğrudan
  çağırma — `spawn_blocking` ile sarmala.

## Fonksiyonel Stil (global "Fonksiyonel Tercih"in Rust karşılığı)
- Global kuraldaki "fonksiyonel tercih" Rust'ta şu demek:
  - Async akışlar: `futures::Stream` + `StreamExt` kombinatörleri
    (`map`, `filter`, `then`, `and_then`, `scan`, `fold`, `buffer_unordered`).
  - Senkron veri: `Iterator` kombinatörleri (`map`/`filter`/`collect`/`fold`/`try_fold`),
    `for`+mutasyon yerine.
  - `Option`/`Result` zincirleri: `map`/`and_then`/`ok_or`/`?`, manuel `match` azalt.
  - Veri + davranış: `enum` + pattern matching; `trait` sadece gerçek polimorfizm gerekince.
- Manuel `loop { recv().await }` yerine Stream pipeline tercih et.
  Mesaj ve event consumer'larını Stream olarak sar; ardışık dönüşümleri pipeline yap.
- Backpressure: `buffer_unordered(n)` veya bounded channel. Unbounded channel kullanma
  (uzun çalışan süreçte bellek patlatır).

### Performans sınırı (global "performans pahalıysa imperatif serbest"in somutu)
- Iterator/Stream kombinatörleri kendi başına maliyetsizdir (zero-cost, monomorphize).
- Maliyet kombinatörden değil; fonksiyonel saflık için eklenen `clone()`,
  `Rc<RefCell>` / `Arc<Mutex>` ve `Box<dyn Fn>`'den gelir.
- I/O-bound akışlarda (consumer, ağ ve dosya I/O) bu maliyet gürültü seviyesinde —
  rahatça fonksiyonel yaz, kopyalamaktan çekinme.
- Hot path / CPU-bound döngüde saflık uğruna allocation ekleme. Sahipliği akıtarak
  (move) çöz; gerekiyorsa imperatif yaz.
- Closure'ları kombinatörlere `impl Fn` (generic) geçir, `dyn` boxed değil.

## Referans Kod (başka dilden Rust'a)
- Başka dildeki referans kod yalnızca DAVRANIŞ/NİYET referansıdır, çevrilecek şablon değil.
- "Bu kod ne yapıyor / hangi problemi çözüyor?" diye düşün; satır satır çevirme (transliteration).
- "Rust'ta bu nasıl yapılır?" diye yeniden tasarla; kaynak dilin desenini taşıma.

Taşıma (yapma):
- OOP sınıf hiyerarşisi / inheritance → körü körüne `trait`'e aktarma; çoğu zaman
  `enum` + pattern matching daha idiomatik.
- Java null / C++ pointer → `Option`/`Result` ile düşün; `unwrap` ile null taklidi yapma.
- Paylaşımlı mutable durum → otomatik `Arc<Mutex>` / `Rc<RefCell>`'e çevirme;
  önce sahiplik/move ile çözülebilir mi bak.
- Exception / try-catch → `Result` + `?` ile yeniden kur, panic'e map etme.
- Defansif kopya (Java clone, C++ copy-ctor) → move/borrow varken `clone` ekleme.
- Getter/setter, builder boilerplate → Rust'ta gereksizse ekleme.

İdiomatik tercih:
- Hata: `Result`/`?`; kütüphanede `thiserror`, uygulamada `anyhow`.
- Kaynak yönetimi: RAII / `Drop`, manuel cleanup değil.
- Şüphedeysen kaynak dilin desenini taşımak yerine idiomatik Rust alternatifini öner,
  nedenini bir cümleyle açıkla. "Kaynak dilde şöyleydi" değil, "Rust'ta bu problemi şöyle çözeriz".

## Yorum Disiplini (Rust somutu)
Global "Yorum Disiplini"nin Rust karşılığı.
- İmza Rust'ta çok şey söyler: parametre tipleri, `-> Result<T, E>` / `Option<T>`,
  `&mut self` (mutasyon), sahiplik, trait bound'ları. Yorum bunların tekrarıysa
  (`fn sum` üstüne `/// returns the sum`) → sil.
- Doc-comment (`///`, `//!`) yalnızca public yüzeyde: imzada görünmeyen yan etki
  (`&mut self` neyi değiştirir), dönüşün anlamı, `# Errors` / `# Panics` / precondition.

## Lint (kuralları zorla)
Crate köküne (`lib.rs` / `main.rs`):
```rust
#![warn(clippy::unwrap_used)]
#![warn(clippy::expect_used)]
#![warn(clippy::panic)]
```
- `make lint` önce `cargo fmt --check`, sonra `clippy --all-targets -- -D warnings`
  koşar; uyarı hatadır. Faz sonunda `make gate`.
- Testte `unwrap`/`expect` serbesttir: repo kökündeki `clippy.toml`
  (`allow-unwrap-in-tests`, `allow-expect-in-tests`).
- Test dışında bilinçli `expect`/`panic!` gerekçesiyle yazılır:
  `#[expect(clippy::expect_used, reason = "…")]`. Gerekçe yorumda değil `reason`'da durur.
