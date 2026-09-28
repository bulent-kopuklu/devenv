# Arayüz: insan yalnız `make <hedef>` yazar. Her bileşen components/<ad>/
# altında, kendi manifest'iyle durur; ürün kodu tek dildir. Bileşen açılınca
# bu dosyaya bağlanır: <hedef>-<ad> reçetesi yazılır, toplu hedef onu çağırır.
# Teslim edilen binary'ler $(BIN)'e yazılır; dist yalnız onu toplar.
#
#   make                                   build, debug, host
#   make build VARIANT=release TARGET=aarch64
#   make test COMPONENTS="api agent"       unit (ve contract)
#   make test-integration                  gerçek dış sistemle, tek süreç
#   make test-evidence                     çok süreç, arıza; EVIDENCE=short|full
#   make gate                              build, lint, test, test-integration, test-evidence
#   make bench                             performans ölçümü, kapının dışında
#   make build-agent                       tek bileşen
#   make dist TARGET=armv7                 release çıktısı → dist/armv7/
#   make clean | distclean                 RUNS'a dokunmaz

VARIANT    ?= debug
TARGET     ?= host
COMPONENTS ?= $(notdir $(wildcard components/*))
RUNS       ?= runs
$(if $(filter $(VARIANT),debug release),,$(error VARIANT=$(VARIANT); seçenekler: debug release))
$(if $(filter $(TARGET),host aarch64 armv7),,$(error TARGET=$(TARGET); seçenekler: host aarch64 armv7))
$(if $(and $(filter-out host,$(TARGET)),$(filter test test-% bench,$(MAKECMDGOALS))),\
  $(error testler yalnız host'ta koşar; TARGET=$(TARGET) için make build))
BIN := $(abspath build)/$(TARGET)/$(VARIANT)/bin

.DEFAULT_GOAL := build
.PHONY: build test test-integration test-evidence bench lint gate dist clean distclean

# Bileşen bağlanana kadar boş geçer.
build test test-integration test-evidence bench lint:
	@:

gate:
	$(MAKE) build
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) test-integration
	$(MAKE) test-evidence

dist:
	$(MAKE) build VARIANT=release
	mkdir -p dist/$(TARGET)
	[ ! -d build/$(TARGET)/release/bin ] || cp -a build/$(TARGET)/release/bin/. dist/$(TARGET)/

clean:
	rm -rf build

distclean: clean
	rm -rf dist
