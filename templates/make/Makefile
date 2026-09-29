# Arayüz: insan yalnız `make <hedef>` yazar. Her bileşen components/<ad>/
# altında kendi Makefile'ıyla durur; kök bir hedefi COMPONENTS'teki her
# bileşene indirir. evidence/ ürünü dışarıdan ölçer; kök onun hedeflerini
# evidence/Makefile'a indirir. Teslim edilen binary'ler $(BIN)'e yazılır;
# dist yalnız onu toplar.
#
#   make                                   build, debug, host
#   make build VARIANT=release TARGET=aarch64
#   make test COMPONENTS="api agent"       unit (ve contract); evidence'ın kendi testleri
#   make test-integration                  gerçek dış sistemle, sahadaki process düzeniyle
#   make evidence:<ad>                     bir bileşenin ya da sistemin evidence'ı; EVIDENCE=short|full
#   make evidence:<ad> SCENARIO="<s> <s>"  yalnız bu senaryolar
#   make evidence:all                      bütün evidence
#   make gate                              build, lint, test, test-integration, evidence:all
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
$(if $(and $(filter-out host,$(TARGET)),$(filter test test-% bench gate evidence:%,$(MAKECMDGOALS))),\
  $(error testler yalnız host'ta koşar; TARGET=$(TARGET) için make build))
BUILD := $(abspath build)
BIN   := $(BUILD)/$(TARGET)/$(VARIANT)/bin

# Bir make çağrısı tek koşu dizini açar; gate'in alt make'leri onu export'tan
# devralır, her evidence dizini kendi $(TEST_RUN)/<dizin> altına yazar.
ifndef TEST_RUN
TEST_RUN := $(abspath $(RUNS))/$(PROJECT)/$(shell date +%Y%m%d-%H%M%S)-$(subst :,-,$(or $(firstword $(MAKECMDGOALS)),build))
endif
export VARIANT TARGET BUILD BIN TEST_RUN

GOALS := test-integration bench

.DEFAULT_GOAL := build
.PHONY: build test lint $(GOALS) evidence\:all gate dist clean distclean

build test lint:
	@for c in $(COMPONENTS); do $(MAKE) -C components/$$c $@ || exit 1; done
	@$(MAKE) -C evidence $@

$(GOALS):
	@for c in $(COMPONENTS); do $(MAKE) -C components/$$c $@ || exit 1; done

evidence\:all:
	@$(MAKE) -C evidence run-all

evidence\:%:
	@$(MAKE) -C evidence run AD=$*

gate:
	$(MAKE) build
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) test-integration
	$(MAKE) evidence:all

dist:
	$(MAKE) build VARIANT=release
	mkdir -p dist/$(TARGET)
	[ ! -d $(BUILD)/$(TARGET)/release/bin ] || cp -a $(BUILD)/$(TARGET)/release/bin/. dist/$(TARGET)/

clean:
	rm -rf build

distclean: clean
	rm -rf dist
	@for c in $(COMPONENTS); do $(MAKE) -C components/$$c distclean || exit 1; done
