# Kök Makefile'dan çağrılır; VARIANT, TARGET, BUILD, BIN ve TEST_RUN oradan
# gelir. Her bileşenin evidence'ı evidence/<bileşen>/, birden çok bileşeni
# kullanan senaryolar evidence/systems/<ad>/ altında kendi Makefile'ıyla
# durur. sysenv/ ortam düzeneğidir, Makefile'ı yoktur.
#
#   make build | lint     her dizinin build'i ya da lint'i; OUT=$(BUILD)/evidence/<dizin>
#   make run AD=<ad>      bir bileşenin ya da sistemin run'ı; RUN=$(TEST_RUN)/<dizin>
#   make run-all          her dizinin run'ı

DIRS  := $(patsubst %/Makefile,%,$(wildcard */Makefile systems/*/Makefile))
match  = $(filter $(AD) systems/$(AD),$(DIRS))

.PHONY: build lint run run-all

build lint:
	@for d in $(DIRS); do $(MAKE) -C $$d $@ OUT=$(BUILD)/evidence/$$d || exit 1; done

run:
	$(if $(match),,$(error evidence: '$(AD)' yok; seçenekler: $(patsubst systems/%,%,$(DIRS))))
	$(if $(word 2,$(match)),$(error evidence: '$(AD)' hem bileşen hem sistem adı))
	@$(MAKE) -C $(match) run RUN=$(TEST_RUN)/$(match)

run-all:
	@for d in $(DIRS); do $(MAKE) -C $$d run RUN=$(TEST_RUN)/$$d || exit 1; done
