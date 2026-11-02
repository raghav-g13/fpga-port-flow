---
id: CHIPYARD-STEP8-PART3-ITER1
repo: CHIPYARD
step: 8
part: 3
iter: 1
parent: FIRESIM-STEP8-PART3-ITER1
timestamp: 2026-08-05T10:31:42.885777+00:00
git_hash: 8b908957e073aa449325e50ab08f069beb008253
---

# step8/part3: Added four lifecycle override methods to XilinxAlveoV80InstanceDeployManager: (A) infrasetup_instance - copies base class logic but uses unload_qdma()/load_qdma() instead of unload_xdma()/load_xdma(),

## Message

Added four lifecycle override methods to XilinxAlveoV80InstanceDeployManager: (A) infrasetup_instance - copies base class logic but uses unload_qdma()/load_qdma() instead of unload_xdma()/load_xdma(), maintaining the flow: copy sim infrastructure -> unload_qdma -> flash_fpgas -> load_qdma -> change_pcie_perms; (B) enumerate_fpgas - copies base class logic with qdma substitution, calls change_all_pcie_perms and create_fpga_database; (C) start_sim_slot - copies base class logic but passes +bar=0x1 instead of +bar=0x0 (V80 uses BAR1 for MMIO); (D) create_fpga_database - follows the CorigineXB10 single-session pattern to avoid hw_server wedge, uses firesim-generate-fpga-db.py (standard, not v2) and references FireSim-xilinx_alveo_v80 driver binary.

## Diff

```diff

```

## Files modified

- `/home/ray/chipyard/sims/firesim/deploy/runtools/run_farm_deploy_managers.py`
