# Node Kuralları

## Makefile'da Node bileşeni
Bileşeni kökteki Makefile'a bağlarken reçeteler şöyledir; komutlar
`components/<ad>/` içinde koşar.
- build ve test'ten önce bağımlılık: `node_modules` yoksa
  `npm install --no-audit --no-fund`.
- `build-<ad>`: `npm run --if-present build`.
- `test-<ad>`: `npm run --if-present test`.
- `lint-<ad>`: kökten `biome check components/<ad>`.
- Çıktı bileşenin kendi dizininde kalır; `dist` onu toplamaz.
- `distclean` bileşen dizinindeki `node_modules/`'ı da siler.
