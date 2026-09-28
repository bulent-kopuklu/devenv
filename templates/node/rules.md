# Node Kuralları

## Makefile'da Node bileşeni
Bileşenin `Makefile`'ı `components/<ad>/`'dadır; komutlar orada koşar. Kaynak
dizini `src/`'dir; `package.json` bileşen dizinindedir.
- build ve test'ten önce bağımlılık: `node_modules` yoksa
  `npm install --no-audit --no-fund`.
- `build`: `npm run --if-present build`.
- `test`: `npm run --if-present test`.
- `lint`: `biome check .`.
- Çıktı bileşenin kendi dizininde kalır; `dist` onu toplamaz.
- `distclean`: bileşen dizinindeki `node_modules/`'ı siler.
