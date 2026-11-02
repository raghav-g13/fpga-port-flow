---
id: FIRESIM-STEP5-PART2-ITER1
repo: FIRESIM
step: 5
part: 2
iter: 1
parent: CHIPYARD-STEP5-PART1-ITER1
timestamp: 2026-08-05T05:50:28.417430+00:00
git_hash: STDERR:
---

# step5/part2: Verified the compiled V80 driver binary (FireSim-xilinx_alveo_v80) with all four checks passing: (1) file confirms ELF 64-bit LSB pie executable, x86-64; (2) ldd with conda LD_LIBRARY_PATH shows all 6

## Message

Verified the compiled V80 driver binary (FireSim-xilinx_alveo_v80) with all four checks passing: (1) file confirms ELF 64-bit LSB pie executable, x86-64; (2) ldd with conda LD_LIBRARY_PATH shows all 6 required shared libraries resolve (libriscv.so, libdwarf.so.1, libelf.so.1, libz.so.1, libstdc++.so.6, libgmp.so.10) with zero 'not found' entries; (3) nm shows no __isoc23 stale glibc symbols; (4) runtime smoke test exits with code 134 (SIGABRT from expected assertion 'tmp_id == id' in fpga_pci_check_file_id at simif_xilinx_alveo_v80.cc:76) and NOT 139 (no segfault), printing expected default parameter messages before the assertion. Binary copied to platform delivery directory with matching MD5 checksum bc0ca41fc860127af97776d97c1d3b44.

## Diff

```diff

STDERR:
error: Could not access 'STDERR:'

[exit code: 1]
```

## Files modified

- `$FIRESIM/platforms/xilinx_alveo_v80/cl_xilinx_alveo_v80-firesim-FireSim-FireSimRocket8GiBDRAMConfig-BaseXilinxAlveoV80Config/driver/FireSim-xilinx_alveo_v80`
