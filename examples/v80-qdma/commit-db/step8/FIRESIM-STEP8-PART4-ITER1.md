---
id: FIRESIM-STEP8-PART4-ITER1
repo: FIRESIM
step: 8
part: 4
iter: 1
parent: CHIPYARD-STEP8-PART3-ITER1
timestamp: 2026-08-05T10:39:00.173940+00:00
git_hash: 5efbc4ef60acec8150813f67e80c00140c9199d6
---

# step8/part4: Created comprehensive dry-run verification test script at $FIRESIM/deploy/tests/test_v80_deploy_manager.py with 78 tests across 4 verification categories: (A) Import & instantiation - verifies XilinxA

## Message

Created comprehensive dry-run verification test script at $FIRESIM/deploy/tests/test_v80_deploy_manager.py with 78 tests across 4 verification categories: (A) Import & instantiation - verifies XilinxAlveoV80InstanceDeployManager imports correctly and all 9 expected methods exist with correct type signatures; (B) QDMA BDF encoding - unit tests _compute_qdma_bdf() with 5 BDF inputs including the 3 required ones (b1:00.0=724992, 3b:00.0=241664, 86:00.1=0x86001) plus edge cases, verifying 5-digit hex formatting; (C) Command sequence audit - validates load_qdma sets qmax before q add before q start, uses mode mm dir bi (not streaming), flash_fpgas does rescan after programming and disconnect before, unload_qdma stops before deleting queues, modprobe uses qdma-pf hyphen convention; (D) C++ driver cross-check - confirms BDF encoding formula (bus<<12|dev<<4|func) matches between simif_xilinx_alveo_v80.cc and Python, BAR index=1, BAR size=32MB=2^25, device pattern /dev/qdmaXXXXX-MM-0 matches queue setup, PCI IDs vendor=0x10ee device=0x903f match. Two bugs were found and fixed during development: regex for C++ BDF pattern needed to match cast-prefixed variable names, and rescan position check was hitting docstring instead of actual sysfs command.

## Diff

```diff

```

## Files modified

- `$FIRESIM/deploy/tests/test_v80_deploy_manager.py`
