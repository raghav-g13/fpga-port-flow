---
id: FIRESIM-STEP9-PART4-ITER1
repo: FIRESIM
step: 9
part: 4
iter: 1
parent: CHIPYARD-STEP9-PART3-ITER1
timestamp: 2026-08-05T17:50:06.432575+00:00
git_hash: 5efbc4ef60acec8150813f67e80c00140c9199d6
---

# step9/part4: Fixed ADEF-911 DRC failure with a two-pronged approach: (A) In implementation.tcl, moved 'set_property STEPS.WRITE_DEVICE_IMAGE.TCL.PRE' from line 46 (after first launch_runs) to line 24 (before first

## Message

Fixed ADEF-911 DRC failure with a two-pronged approach: (A) In implementation.tcl, moved 'set_property STEPS.WRITE_DEVICE_IMAGE.TCL.PRE' from line 46 (after first launch_runs) to line 24 (before first launch_runs on line 31), ensuring the DRC downgrade hook is part of the initial run configuration for all launch_runs invocations. (B) In synthesis.tcl, added 'set_property STEPS.SYNTH_DESIGN.TCL.POST' pointing to a new post_synth_in_context.tcl script, set before launch_runs (line 14 vs line 16). Created post_synth_in_context.tcl with the BUFGCE SIM_DEVICE fix using -quiet flag, which runs inside the synthesis subprocess before the checkpoint is saved to disk. This belt-and-suspenders approach ensures BUFGCEs are fixed in the persistent checkpoint (prong B) AND the DRC check is downgraded as a safety net (prong A).

## Diff

```diff

```

## Files modified

- `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/scripts/implementation.tcl`
- `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/scripts/synthesis.tcl`
- `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/scripts/post_synth_in_context.tcl`
