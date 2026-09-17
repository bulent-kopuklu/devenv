
manifest_files += CMakeLists.txt
manifest_CMakeLists.txt := cpp

# C prefix'i devshell'in nix cross derleyicisinden gelir (armv7l).
ccpfx_aarch64  := aarch64-unknown-linux-gnu-
ccpfx_armv7    := armv7l-unknown-linux-gnueabihf-
cmake_type_debug   := Debug
cmake_type_release := Release
cpp_dir   = $(OUT)/cmake/$1
cpp_cross = $(if $(CROSS),-DCMAKE_SYSTEM_NAME=Linux -DCMAKE_SYSTEM_PROCESSOR=$(TARGET) \
              -DCMAKE_C_COMPILER=$(ccpfx_$(TARGET))clang -DCMAKE_CXX_COMPILER=$(ccpfx_$(TARGET))clang++)
cpp_build = cmake -S components/$1 -B $(cpp_dir) -G Ninja -DCMAKE_BUILD_TYPE=$(cmake_type_$(VARIANT)) \
              -DCMAKE_INSTALL_PREFIX=$(OUT) $(cpp_cross) \
            && cmake --build $(cpp_dir) && cmake --install $(cpp_dir)
cpp_test  = $(call cpp_build,$1) && ctest --test-dir $(cpp_dir) --output-on-failure
cpp_lint  = $(call cpp_build,$1) && run-clang-tidy -quiet -p $(cpp_dir) $(abspath components/$1)
