# V80 Driver Clean Rebuild - SUCCESS

**Date**: 2026-08-04
**Step**: Driver compilation verification - Part 1

## Problem
Stale .o files compiled in a different environment (glibc sysroot at /home/ray/chipyard/) 
contained references to `__isoc23_strtol` which doesn't exist in the container's glibc 2.35.

## Solution
1. Cleaned all stale .o files from `$OUT_BUILD_DIR` with `find -name '*.o' -delete`
2. Removed old binary `$OUT_DIR/FireSim-xilinx_alveo_v80`
3. Copied `FireSim-generated.const.h` from `$GEN_DIR` to `$OUT_BUILD_DIR`
4. Rebuilt using inner MIDAS Makefile with proper CXXFLAGS and LDFLAGS for conda-only platforms
5. Build completed successfully with `make` exit code 0

## Build Details
- **Compiler**: g++ with C++20 standard
- **Binary size**: 12,536,264 bytes (12.5 MB)
- **Binary type**: ELF 64-bit LSB pie executable, x86-64, with debug_info, not stripped
- **No __isoc23_strtol references**: verified with `nm -u`
- **All shared libraries resolve**: verified with `ldd`
- **V80-specific file (simif_xilinx_alveo_v80.cc)**: compiled with zero warnings
- **Pre-existing warnings**: format warnings in cospike_impl.cc, unused-value in firesim_tsi/dtm.cc, sign-compare in ctc.cc — all from testchipip/firechip, not V80-specific

## Key Flags Used
- CXXFLAGS: includes testchipip/firechip/bridgestubs headers, GEN_DIR, -DFIRESIM, -O2, -g
- LDFLAGS: links against $RISCV/lib (riscv, dwarf, elf, z, rt), rpath=$ORIGIN
