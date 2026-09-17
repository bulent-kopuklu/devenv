# Her bileşen components/<ad>/ altında, tek dilde, kendi manifest'iyle durur.
# Bu dosya bileşenleri listelemez: dili manifest'ten okur. Yeni bileşen için
# dizini açmak yeter. dist yalnız bin/'i toplar.
#
#   make                                   build, debug, host
#   make build VARIANT=release TARGET=aarch64
#   make test COMPONENTS="api agent"
#   make build-agent                       tek bileşen
#   make dist TARGET=armv7                 release çıktısı → dist/armv7/
#   make gate                              sıfırdan build, lint, test, test-integration
#   make clean | distclean

VARIANT    ?= debug
TARGET     ?= host
COMPONENTS ?= $(notdir $(wildcard components/*))
BUILD_DIR  ?= build
DIST_DIR   ?= dist

VARIANTS := debug release
TARGETS  := host aarch64 armv7
$(if $(filter $(VARIANT),$(VARIANTS)),,$(error VARIANT=$(VARIANT); seçenekler: $(VARIANTS)))
$(if $(filter $(TARGET),$(TARGETS)),,$(error TARGET=$(TARGET); seçenekler: $(TARGETS)))

BUILD := $(abspath $(BUILD_DIR))
OUT   := $(BUILD)/$(TARGET)/$(VARIANT)
BIN   := $(OUT)/bin
CROSS := $(filter-out host,$(TARGET))

# Dil parçaları manifest dosyasını ve distclean'in sileceği dizinleri buraya ekler.
manifest_files :=
distclean_dirs :=
manifests = $(notdir $(wildcard $(addprefix components/$1/,$(manifest_files))))
kind = $(if $(filter 1,$(words $(call manifests,$1))),$(manifest_$(call manifests,$1)),$(error components/$1: tek manifest bekleniyor ($(manifest_files)), bulunan: $(or $(call manifests,$1),yok)))
