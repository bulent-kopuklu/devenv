# Arayüz: insan yalnız `make <hedef>` yazar. Her bileşen components/<ad>/
# altında kendi Makefile'ıyla durur; kök bir hedefi COMPONENTS'teki her
# bileşene indirir. Teslim edilen binary'ler $(BIN)'e yazılır; dist yalnız
# onu toplar.
#
#   make                                   build, debug, host
#   make build VARIANT=release TARGET=aarch64
#   make test COMPONENTS="api agent"       unit (ve contract)
#   make test-integration                  gerçek dış sistemle, tek süreç
#   make test-evidence                     çok süreç, arıza; EVIDENCE=short|full
#   make gate                              build, lint, test, test-integration, test-evidence
#   make bench                             performans ölçümü, kapının dışında
#   make build COMPONENTS=agent            tek bileşen
#   make dist TARGET=armv7                 release çıktısı → dist/armv7/
#   make clean | distclean                 RUNS'a dokunmaz
#   RUNS=~/runs make gate                  koşu çıktısının kökü; verilmezse ~/.local/state/runs

VARIANT    ?= debug
TARGET     ?= host
COMPONENTS ?= $(patsubst components/%/Makefile,%,$(wildcard components/*/Makefile))
RUNS       ?= $(or $(XDG_STATE_HOME),$(HOME)/.local/state)/runs
PROJECT    := {{NAME}}
$(if $(filter $(VARIANT),debug release),,$(error VARIANT=$(VARIANT); seçenekler: debug release))
$(if $(filter $(TARGET),host aarch64 armv7),,$(error TARGET=$(TARGET); seçenekler: host aarch64 armv7))
$(if $(and $(filter-out host,$(TARGET)),$(filter test test-% bench,$(MAKECMDGOALS))),\
  $(error testler yalnız host'ta koşar; TARGET=$(TARGET) için make build))
BUILD := $(abspath build)
BIN   := $(BUILD)/$(TARGET)/$(VARIANT)/bin

# Bir make çağrısı tek koşu dizini açar; gate'in alt make'leri onu export'tan
# devralır, her bileşen kendi $(TEST_RUN)/<ad>/<hedef> altına yazar.
ifndef TEST_RUN
TEST_RUN := $(abspath $(RUNS))/$(PROJECT)/$(shell date +%Y%m%d-%H%M%S)-$(or $(firstword $(MAKECMDGOALS)),build)
endif
export VARIANT TARGET BUILD BIN TEST_RUN

GOALS := build test test-integration test-evidence bench lint

.DEFAULT_GOAL := build
.PHONY: $(GOALS) gate dist clean distclean

$(GOALS):
	@for c in $(COMPONENTS); do $(MAKE) -C components/$$c $@ || exit 1; done

gate:
	$(MAKE) build
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) test-integration
	$(MAKE) test-evidence

dist:
	$(MAKE) build VARIANT=release
	mkdir -p dist/$(TARGET)
	[ ! -d $(BUILD)/$(TARGET)/release/bin ] || cp -a $(BUILD)/$(TARGET)/release/bin/. dist/$(TARGET)/

clean:
	rm -rf build

distclean: clean
	rm -rf dist
	@for c in $(COMPONENTS); do $(MAKE) -C components/$$c distclean || exit 1; done
