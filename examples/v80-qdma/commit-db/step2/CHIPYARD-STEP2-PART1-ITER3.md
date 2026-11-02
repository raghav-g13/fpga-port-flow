---
id: CHIPYARD-STEP2-PART1-ITER3
repo: CHIPYARD
step: 2
part: 1
iter: 3
parent: FIRESIM-STEP2-PART1-ITER3
timestamp: 2026-08-04T18:13:51.704856+00:00
git_hash: STDERR:
---

# step2/part1: Added bar_test0 test case to tests_firesim.vh that exercises F1Shim SimulationMaster registers via BAR1 (user_bar). The test reads PRESENCE_READ (0x224, expects 0x46697265), INIT_DONE (0x220, expects 

## Message

Added bar_test0 test case to tests_firesim.vh that exercises F1Shim SimulationMaster registers via BAR1 (user_bar). The test reads PRESENCE_READ (0x224, expects 0x46697265), INIT_DONE (0x220, expects 1), writes 0xDEADBEEF to PRESENCE_WRITE (0x228) and verifies readback via PRESENCE_READ, and reads PeekPoke DONE (0x1D0) for bus connectivity. All reads include X-value checking using Verilog-compatible (^val === 1'bx) pattern instead of SystemVerilog $isunknown(). Test reports PASSED/FAILED and calls $finish. Placed before qdma_mm_firesim_test0 block.

## Diff

```diff

STDERR:
error: Could not access 'STDERR:'

[exit code: 1]
```

## Files modified

- `platforms/xilinx_alveo_v80/cl_firesim/verif/tests_firesim.vh`
