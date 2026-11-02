---
id: CHIPYARD-STEP1-PART1-ITER1
repo: CHIPYARD
step: 1
part: 1
iter: 1
parent: FIRESIM-STEP1-PART1-ITER1
timestamp: 2026-08-04T04:36:23.564894+00:00
git_hash: STDERR:
---

# step1/part1: Created gen_vcs_firesim.tcl to export VCS simulation scripts from the existing firesim.xpr Vivado project. The script: (1) auto-detects CL_DIR via glob or accepts it as argument, (2) opens firesim.xpr

## Message

Created gen_vcs_firesim.tcl to export VCS simulation scripts from the existing firesim.xpr Vivado project. The script: (1) auto-detects CL_DIR via glob or accepts it as argument, (2) opens firesim.xpr, (3) applies PIPESIM=TRUE patches to EP sim wrapper files (bd_70da_cpm_0_0.sv under design_1/), (4) applies PIPESIM_CLK_MASTER=TRUE patch to RP sim wrapper (bd_e4ca_cpm_0_0.sv under design_rp/), (5) calls export_simulation -simulator vcs with lib_map_path pointing to vcs_xilinx_lib. Used a recursive find_files Tcl proc since Tcl glob does not support ** recursive matching. Also fixed synopsys_sim.setup to replace /home/ray/chipyard paths with /home/ray/chipyard paths (42 library path entries updated). Fixed auto-detect path from ../../.. (3 levels) to ../.. (2 levels) to correctly reach the xilinx_alveo_v80/ directory from verif/.

## Diff

```diff

STDERR:
error: Could not access 'STDERR:'

[exit code: 1]
```

## Files modified

- `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/verif/gen_vcs_firesim.tcl`
- `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/verif/vcs_xilinx_lib/synopsys_sim.setup`
