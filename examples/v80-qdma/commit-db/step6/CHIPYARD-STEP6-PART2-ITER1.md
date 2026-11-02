---
id: CHIPYARD-STEP6-PART2-ITER1
repo: CHIPYARD
step: 6
part: 2
iter: 1
parent: FIRESIM-STEP6-PART2-ITER1
timestamp: 2026-08-05T06:30:45.708153+00:00
git_hash: STDERR:
---

# step6/part2: Built the Verilator metasimulation model (VFireSim) from existing Golden Gate output using the inner Makefile at $FIRESIM/sim/midas/src/main/cc/Makefile. The initial build failed because Verilator cou

## Message

Built the Verilator metasimulation model (VFireSim) from existing Golden Gate output using the inner Makefile at $FIRESIM/sim/midas/src/main/cc/Makefile. The initial build failed because Verilator could not find the 'plusarg_reader' and 'AbstractClockGate' modules — these are black box Verilog files in $GEN_DIR that the inner Makefile doesn't automatically include. Fixed by adding '-y $GEN_DIR' to VERILATOR_FLAGS so Verilator auto-discovers module files in that directory. Also ensured LDFLAGS includes '-L$CONDA_PREFIX/lib' since libdwarf.so, libelf.so, and libgmp.so are in $CONDA_PREFIX/lib (not $RISCV/lib). No source files were modified — only build invocation flags were adjusted.

## Diff

```diff

STDERR:
error: Could not access 'STDERR:'

[exit code: 1]
```

## Files modified

- (none)
