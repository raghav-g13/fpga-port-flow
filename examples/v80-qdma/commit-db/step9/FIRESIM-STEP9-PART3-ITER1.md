---
id: FIRESIM-STEP9-PART3-ITER1
repo: FIRESIM
step: 9
part: 3
iter: 1
parent: CHIPYARD-STEP9-PART2-ITER1
timestamp: 2026-08-05T17:44:48.562410+00:00
git_hash: 5efbc4ef60acec8150813f67e80c00140c9199d6
---

# step9/part3: Configured V80 for fastest possible verification build. (A) config_build_recipes.yaml: changed fpga_frequency from 75 to 10 MHz and build_strategy from TIMING to Flow_Quick for the V80 recipe. (B) con

## Message

Configured V80 for fastest possible verification build. (A) config_build_recipes.yaml: changed fpga_frequency from 75 to 10 MHz and build_strategy from TIMING to Flow_Quick for the V80 recipe. (B) config_build.yaml: changed builds_to_run to xilinx_alveo_v80_firesim_rocket_singlecore_no_nic and set default_build_dir to /home/ray/chipyard/sims/firesim/platforms/xilinx_alveo_v80/cl_firesim. (C) externally_provisioned.yaml: set matching default_build_dir. Also added Flow_Quick to BuildStrategy enum in buildconfig.py and created strategy_Flow_Quick.tcl (skips opt, phys_opt, and post-route phys_opt; uses Quick directives for place and route).

## Diff

```diff

```

## Files modified

- `$FIRESIM/deploy/config_build_recipes.yaml`
- `$FIRESIM/deploy/config_build.yaml`
- `$FIRESIM/deploy/build-farm-recipes/externally_provisioned.yaml`
- `$FIRESIM/deploy/buildtools/buildconfig.py`
- `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/scripts/strategies/strategy_Flow_Quick.tcl`
