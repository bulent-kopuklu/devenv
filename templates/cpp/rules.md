# C++ Kuralları

## Makefile'da C++ bileşeni
Bileşenin `Makefile`'ı `components/<ad>/`'dadır; komutlar orada koşar. Kaynak
dizini `src/`'dir; `CMakeLists.txt` bileşen dizinindedir. Build dizini
`$(BUILD)/$(TARGET)/$(VARIANT)/cmake/<ad>`'dır; `<ad>` bileşenin adıdır,
`$(notdir $(CURDIR))`.
- `build`: `cmake -S . -B <build dizini> -G Ninja
  -DCMAKE_BUILD_TYPE=<Debug|Release> -DCMAKE_INSTALL_PREFIX=$(BUILD)/$(TARGET)/$(VARIANT)`,
  sonra `cmake --build <build dizini>` ve `cmake --install <build dizini>`.
  Install çalıştırılabilirleri `$(BIN)`'e koyar.
- `TARGET` host değilse configure'a eklenir: `-DCMAKE_SYSTEM_NAME=Linux
  -DCMAKE_SYSTEM_PROCESSOR=<target> -DCMAKE_C_COMPILER=<önek>clang
  -DCMAKE_CXX_COMPILER=<önek>clang++`. Önek devshell'in nix cross
  derleyicisinden gelir: aarch64 `aarch64-unknown-linux-gnu-`, armv7
  `armv7l-unknown-linux-gnueabihf-`.
- `test`: önce build, sonra `ctest --test-dir <build dizini> --output-on-failure`.
- `lint`: önce build (clang-tidy `compile_commands.json`'ı build dizininden
  okur), sonra `run-clang-tidy -quiet -p <build dizini> $(CURDIR)/src`.
- `distclean`: boş.
