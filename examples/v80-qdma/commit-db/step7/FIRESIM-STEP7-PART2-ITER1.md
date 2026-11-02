---
id: FIRESIM-STEP7-PART2-ITER1
repo: FIRESIM
step: 7
part: 2
iter: 1
parent: CHIPYARD-STEP7-PART1-ITER1
timestamp: 2026-08-05T07:16:38.071341+00:00
git_hash: STDERR:
---

# step7/part2: Created a placeholder bitstream tarball from the debug PDI and added V80 HWDB entry to config_hwdb.yaml. Step A: Created staging directory at $FIRESIM/deploy/built-hwdb-entries/xilinx_alveo_v80_firesi

## Message

Created a placeholder bitstream tarball from the debug PDI and added V80 HWDB entry to config_hwdb.yaml. Step A: Created staging directory at $FIRESIM/deploy/built-hwdb-entries/xilinx_alveo_v80_firesim_rocket_singlecore_no_nic/, copied firesim_debug.pdi as firesim.pdi, wrote metadata file with build/deploy quintuplets, and created firesim.tar.gz tarball. Step B: Appended the xilinx_alveo_v80_firesim_rocket_singlecore_no_nic HWDB entry after the DOCREF END marker in config_hwdb.yaml with bitstream_tar (file:// URI), deploy_quintuplet_override (null), and custom_runtime_config (null).

## Diff

```diff

STDERR:
error: Could not access 'STDERR:'

[exit code: 1]
```

## Files modified

- `$FIRESIM/deploy/config_hwdb.yaml`
- `$FIRESIM/deploy/built-hwdb-entries/xilinx_alveo_v80_firesim_rocket_singlecore_no_nic/xilinx_alveo_v80/firesim.pdi`
- `$FIRESIM/deploy/built-hwdb-entries/xilinx_alveo_v80_firesim_rocket_singlecore_no_nic/xilinx_alveo_v80/metadata`
- `$FIRESIM/deploy/built-hwdb-entries/xilinx_alveo_v80_firesim_rocket_singlecore_no_nic/firesim.tar.gz`
