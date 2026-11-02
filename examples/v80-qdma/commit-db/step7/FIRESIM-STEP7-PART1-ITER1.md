---
id: FIRESIM-STEP7-PART1-ITER1
repo: FIRESIM
step: 7
part: 1
iter: 1
parent: BASE
timestamp: 2026-08-05T07:13:06.426216+00:00
git_hash: STDERR:
---

# step7/part1: Registered the V80 platform in the firesim managerinit dispatch logic. Two changes to $FIRESIM/deploy/firesim: (1) Appended `or args.platform == 'xilinx_alveo_v80'` to the elif condition on line 187 s

## Message

Registered the V80 platform in the firesim managerinit dispatch logic. Two changes to $FIRESIM/deploy/firesim: (1) Appended `or args.platform == 'xilinx_alveo_v80'` to the elif condition on line 187 so the V80 platform is routed through the externally-provisioned run farm path (same as other Alveo/Corigine platforms). (2) Added `'xilinx_alveo_v80': 'XilinxAlveoV80InstanceDeployManager'` to the deploy_manager_map dictionary so the correct deploy manager class is selected at runtime.

## Diff

```diff

STDERR:
error: Could not access 'STDERR:'

[exit code: 1]
```

## Files modified

- `/home/ray/chipyard/sims/firesim/deploy/firesim`
