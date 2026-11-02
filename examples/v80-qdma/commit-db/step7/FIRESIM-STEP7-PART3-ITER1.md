---
id: FIRESIM-STEP7-PART3-ITER1
repo: FIRESIM
step: 7
part: 3
iter: 1
parent: CHIPYARD-STEP7-PART2-ITER1
timestamp: 2026-08-05T07:23:29.901393+00:00
git_hash: STDERR:
---

# step7/part3: Updated config_runtime.yaml to set default_hw_config to 'xilinx_alveo_v80_firesim_rocket_singlecore_no_nic' (was 'midasexamples_gcd'). Also added the V80 build recipe entry to config_build_recipes.yam

## Message

Updated config_runtime.yaml to set default_hw_config to 'xilinx_alveo_v80_firesim_rocket_singlecore_no_nic' (was 'midasexamples_gcd'). Also added the V80 build recipe entry to config_build_recipes.yaml (PLATFORM: xilinx_alveo_v80, TARGET_CONFIG: WithDefaultFireSimBridges_WithFireSimConfigTweaks_chipyard.RocketConfig, PLATFORM_CONFIG: BaseXilinxAlveoV80Config, bit_builder_recipe: bit-builder-recipes/xilinx_alveo_v80.yaml) to ensure all 4 consistency checks pass.

## Diff

```diff

STDERR:
error: Could not access 'STDERR:'

[exit code: 1]
```

## Files modified

- `$FIRESIM/deploy/config_runtime.yaml`
- `$FIRESIM/deploy/config_build_recipes.yaml`
