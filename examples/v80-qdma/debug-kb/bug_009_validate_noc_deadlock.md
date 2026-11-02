# Bug 009: Post-Synthesis Deadlock in Vivado 2025.1 for Versal (SOLVED)

## Symptom
After synthesis completes successfully (0 errors), Vivado hangs indefinitely. All threads are in `futex_wait_queue` or `hrtimer_nanosleep`. CPU time barely advances. The process reads ~84KB/s from shared memory (polling) but writes nothing. No DCP checkpoint is written.

## Environment
- Vivado 2025.1
- Part: xcv80-lsva4737-2MHP-e-S (Versal ACAP V80)
- Design uses CPM5 with QDMA (via Versal CIPS IP) and dual AXI NoC instances
- Container environment with locale workaround

## Reproducibility
**100% reproducible** — observed on attempts 1-11 (with varying symptoms depending on workarounds tried).

## Root Cause (CONFIRMED)
The `synth_design` command internally launches a `parallel_synth_helper` process controlled by the `synth.enableParallelHelperSpawn` parameter. After synthesis completes, this helper process dies, but the main Vivado thread is waiting on a futex for the dead helper — causing permanent deadlock.

**Discovery path:**
1. Used `strings` on `libxv_synth.so` searching for "helper" 
2. Found `synth.enableParallelHelperSpawn` parameter
3. Found valid values from the ERROR message: `all`, `none`, `linux`, `windows`
4. Setting `none` prevents the helper from being launched entirely

**Earlier misdiagnosis:** Initially attributed to `validate_noc` deadlock (NoC validation thread deadlock). The actual root cause is the parallel helper process lifecycle bug — validate_noc wasn't even the issue.

## Fix (VERIFIED)
Set `synth.enableParallelHelperSpawn none` BEFORE `synth_design` runs:

```tcl
# In pre_synth_noc_fix.tcl (TCL.PRE hook for SYNTH_DESIGN)
# or in standalone_synth.tcl

set_param synth.enableParallelHelperSpawn none
```

### Important: Value MUST be `none`, NOT `false`
- `false` → ERROR: [Designutils 20-2125] Illegal value specified; synth_design fails
- `none` → Correct; no helper launched, no deadlock

### Additional workarounds applied (defense in depth):
```tcl
set_param general.usePosixSpawnForFork 0     # Disable posix_spawn
set_param general.maxThreads 1               # Limit threads
catch {set_param synth.maxThreads 0}         # Limit synth threads
catch {set_param noc.enableCompil 0}         # Disable NoC compiler
catch {set_param noc.skipcheckNOCSolutionDirty 1}
catch {set_param noc.skipNOCFreqDrc 1}
catch {set_param noc.disableConfigMerging 1}
```

## Verification
**Attempt 12** (standalone_synth.tcl with `enableParallelHelperSpawn none`):
- No parallel_synth_helper process launched
- synth_design completed successfully (Checksum: 6b841b0d)
- 0 Errors, 2 Critical Warnings, 308 Warnings
- DCP written: overall_fpga_top.dcp (95 MB)
- Total time: cpu = 00:39:54 ; elapsed = 00:25:39
- Vivado exited cleanly

## Attempts Summary
| # | Approach | Result |
|---|----------|--------|
| 1-8 | validate_noc bypass, thread limits, various params | Deadlocked (helper still running) |
| 9 | usePosixSpawnForFork=0 + synth.maxThreads=0 | Helper still launched, deadlocked |
| 10 | isSynthRun=false | Helper still launched |
| 11 | enableParallelHelperSpawn=false | Helper NOT launched, but `false` is invalid value → ERROR |
| 12 | **enableParallelHelperSpawn=none** | **SUCCESS — no helper, no deadlock, DCP written** |

## Files Modified
- `scripts/pre_synth_noc_fix.tcl` — TCL.PRE hook with all workarounds
- `scripts/synthesis.tcl` — sets TCL.PRE property and synthesis flow
- Both template (cl_firesim) and build copy (cl_<quintuplet>) updated

## Key Knowledge
- `synth.enableParallelHelperSpawn` valid values: `all`, `none`, `linux`, `windows`
- The parallel helper is a separate Vivado process for parallel synthesis
- Found via: `strings /ecad/tools/xilinx/2025.1/Vivado/lib/lnx64.o/libxv_synth.so | grep -i helper`
- This is likely a Vivado 2025.1 bug specific to Versal parts in containerized environments
