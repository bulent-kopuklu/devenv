
manifest_files += package.json
manifest_package.json := node
distclean_dirs += components/*/node_modules

# node bileşeninin çıktısı kendi dizininde kalır; dist onu toplamaz.
node_deps  = cd components/$1 && { [ -d node_modules ] || npm install --no-audit --no-fund; }
node_build = $(node_deps) && npm run --if-present build
node_test  = $(node_deps) && npm run --if-present test
node_lint  = biome check components/$1
