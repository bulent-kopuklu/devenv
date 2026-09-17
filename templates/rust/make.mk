
manifest_files += Cargo.toml
manifest_Cargo.toml := rust
distclean_dirs += components/*/target

# Cargo'nun kendi dizin düzeni var (<triple>/<profil>); target dizini bütün
# hedeflere ortak, bağımlılıklar bir kez derlenir. Çalıştırılabilirler bin/'e
# kopyalanır ki dist her dil için aynı yerden toplasın. Triple rustup'tan gelir.
triple_aarch64 := aarch64-unknown-linux-gnu
triple_armv7   := armv7-unknown-linux-gnueabihf
cargo       = cargo $2 --manifest-path components/$1/Cargo.toml --target-dir $(BUILD)/cargo
rust_profile = $(BUILD)/cargo/$(if $(CROSS),$(triple_$(TARGET))/)$(VARIANT)
rust_build  = $(call cargo,$1,build) $(if $(CROSS),--target $(triple_$(TARGET))) $(if $(filter release,$(VARIANT)),--release) \
              && find $(rust_profile) -maxdepth 1 -type f -executable ! -name '*.*' -exec cp -t $(BIN) {} +
rust_test   = $(call cargo,$1,test) $(if $(filter release,$(VARIANT)),--release)
rust_lint   = $(call cargo,$1,clippy) --all-targets -- -D warnings
