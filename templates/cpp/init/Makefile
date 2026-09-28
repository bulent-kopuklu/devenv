NAME := $(notdir $(CURDIR))
BDIR := $(BUILD)/$(TARGET)/$(VARIANT)/cmake/$(NAME)
TYPE.debug   := Debug
TYPE.release := Release
CROSS.aarch64 := -DCMAKE_SYSTEM_NAME=Linux -DCMAKE_SYSTEM_PROCESSOR=aarch64 \
  -DCMAKE_C_COMPILER=aarch64-unknown-linux-gnu-clang -DCMAKE_CXX_COMPILER=aarch64-unknown-linux-gnu-clang++
CROSS.armv7   := -DCMAKE_SYSTEM_NAME=Linux -DCMAKE_SYSTEM_PROCESSOR=armv7 \
  -DCMAKE_C_COMPILER=armv7l-unknown-linux-gnueabihf-clang -DCMAKE_CXX_COMPILER=armv7l-unknown-linux-gnueabihf-clang++

.PHONY: build test test-integration test-evidence bench lint distclean

build:
	cmake -S . -B $(BDIR) -G Ninja -DCMAKE_BUILD_TYPE=$(TYPE.$(VARIANT)) \
	  -DCMAKE_INSTALL_PREFIX=$(BUILD)/$(TARGET)/$(VARIANT) $(CROSS.$(TARGET))
	cmake --build $(BDIR)
	cmake --install $(BDIR)

test: build
	ctest --test-dir $(BDIR) --output-on-failure

lint: build
	run-clang-tidy -quiet -p $(BDIR) $(CURDIR)/src

test-integration test-evidence bench distclean:
	@:
