---
id: CHIPYARD-STEP8-PART2-ITER1
repo: CHIPYARD
step: 8
part: 2
iter: 1
parent: FIRESIM-STEP8-PART2-ITER1
timestamp: 2026-08-05T10:25:10.625631+00:00
git_hash: 8b908957e073aa449325e50ab08f069beb008253
---

# step8/part2: All four required methods already exist in XilinxAlveoV80InstanceDeployManager and were verified correct: (1) _compute_qdma_bdf() splits a BDF string like 'b1:00.0' and computes (bus<<12)|(device<<4)|

## Message

All four required methods already exist in XilinxAlveoV80InstanceDeployManager and were verified correct: (1) _compute_qdma_bdf() splits a BDF string like 'b1:00.0' and computes (bus<<12)|(device<<4)|function, matching the driver convention in simif_xilinx_alveo_v80.cc. (2) load_qdma() loads qdma-pf module if not loaded, reads FPGA DB, sets qmax to 512, adds and starts MM queue 0 bidirectional for each slot, then chmods /dev/qdma*. (3) unload_qdma() tears down queues with warn_only context manager for graceful failure, then unloads qdma-pf module. (4) flash_fpgas() overrides base class: disconnects all FPGAs, programs via Vivado batch, waits 10s for PCIe link re-training, does full bus rescan (not per-BDF reconnect since BDF may change after Versal reprogramming), retries rescan up to 30s, and enables memory-mapped transfers via setpci.

## Diff

```diff

```

## Files modified

- `$FIRESIM/deploy/runtools/run_farm_deploy_managers.py`
