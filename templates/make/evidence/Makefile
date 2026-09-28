# Kök Makefile'dan çağrılır; VARIANT, TARGET, BUILD, BIN ve TEST_RUN oradan
# gelir. Her bileşenin evidence'ı evidence/<bileşen>/, birden çok bileşeni
# kullanan senaryolar evidence/systems/<ad>/ altında kendi Makefile'ıyla
# durur. sysenv/'in Makefile'ı build, test ve lint'e girer, run'a girmez.
# COMPONENTS komut satırından verilirse build, test ve lint yalnız o
# bileşenlerin dizinlerine iner.
#
#   make build | test | lint   her dizine; OUT=$(BUILD)/evidence/<dizin>
#   make run AD=<ad>           bir bileşenin ya da sistemin run'ı; RUN=$(TEST_RUN)/<dizin>
#   make run-all               sysenv dışındaki her dizinin run'ı

DIRS     := $(patsubst %/Makefile,%,$(wildcard */Makefile systems/*/Makefile))
RUNNABLE := $(filter-out sysenv,$(DIRS))
SCOPE    := $(if $(COMPONENTS),$(filter $(COMPONENTS),$(DIRS)),$(DIRS))
match     = $(filter $(AD) systems/$(AD),$(RUNNABLE))

.PHONY: build test lint run run-all

build test lint:
	@for d in $(SCOPE); do $(MAKE) -C $$d $@ OUT=$(BUILD)/evidence/$$d || exit 1; done

run:
	$(if $(match),,$(error evidence: '$(AD)' yok; seçenekler: $(patsubst systems/%,%,$(RUNNABLE))))
	$(if $(word 2,$(match)),$(error evidence: '$(AD)' hem bileşen hem sistem adı))
	@$(MAKE) -C $(match) run RUN=$(TEST_RUN)/$(match)

run-all:
	@for d in $(RUNNABLE); do $(MAKE) -C $$d run RUN=$(TEST_RUN)/$$d || exit 1; done
