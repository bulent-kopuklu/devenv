
.DEFAULT_GOAL := build
.PHONY: build test lint dist gate test-integration clean distclean

build: $(addprefix build-,$(COMPONENTS))
test:  $(addprefix test-,$(COMPONENTS))
lint:  $(addprefix lint-,$(COMPONENTS))

build-%: | $(BIN)
	$(call $(call kind,$*)_build,$*)

test-%:
	$(if $(CROSS),$(error test yalnız host'ta koşar; TARGET=$(TARGET) için make build))
	$(call $(call kind,$*)_test,$*)

lint-%:
	$(call $(call kind,$*)_lint,$*)

$(BIN):
	mkdir -p $@

dist:
	$(MAKE) build VARIANT=release
	mkdir -p $(DIST_DIR)/$(TARGET)
	cp -a $(BUILD)/$(TARGET)/release/bin/. $(DIST_DIR)/$(TARGET)/

# Faz kapısı: sıfırdan, sırayla. test-integration'ı proje tanımlar; tanımlanana
# kadar kapı kırmızıdır.
gate:
	$(MAKE) distclean
	$(MAKE) build
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) test-integration

test-integration:
	@echo "test-integration tanımlı değil: Makefile'da bu hedefi projenin entegrasyon testiyle doldur" >&2; exit 1

clean:
	rm -rf $(BUILD_DIR)

distclean: clean
	rm -rf $(DIST_DIR) $(distclean_dirs)
