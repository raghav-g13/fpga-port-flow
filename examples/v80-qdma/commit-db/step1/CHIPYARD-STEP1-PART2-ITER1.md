---
id: CHIPYARD-STEP1-PART2-ITER1
repo: CHIPYARD
step: 1
part: 2
iter: 1
parent: FIRESIM-STEP1-PART2-ITER1
timestamp: 2026-08-04T05:42:02.306603+00:00
git_hash: STDERR:
---

# step1/part2: Created run_vcs.sh wrapper script for VCS simulation of V80 platform. The script handles: (1) VCS shebang patching (dash→bash), (2) /usr/bin/time wrapper creation, (3) libncurses.so.5 compatibility sy

## Message

Created run_vcs.sh wrapper script for VCS simulation of V80 platform. The script handles: (1) VCS shebang patching (dash→bash), (2) /usr/bin/time wrapper creation, (3) libncurses.so.5 compatibility symlink, (4) environment setup (VCS_HOME, VCS_ARCH_OVERRIDE, LD_LIBRARY_PATH, RDI_DATADIR), (5) argument parsing (compile|elaborate|simulate|all), (6) runtime patching of Vivado-generated board.sh (adds -Xcheck_p1800_2009=char, +define+FIRESIM_EP=, +define+SIMULATION=, elaborate flags). Also added FIRESIM_EP ifdef guard in usp_pci_exp_usrapp_tx.v around COMPARE_DATA_H2C task (247 XMRE cross-module references to non-existent axi_bram_ctrl_0), and guarded sample_tests.vh inclusion in tests.vh. VCS compile succeeds (0 errors, 30 warnings), VCS elaborate succeeds (0 errors, 581 warnings), board_simv binary (ELF 64-bit, 1.9MB) produced successfully.

## Diff

```diff

STDERR:
error: Could not access 'STDERR:'

[exit code: 1]
```

## Files modified

- `platforms/xilinx_alveo_v80/cl_firesim/verif/run_vcs.sh`
- `platforms/xilinx_alveo_v80/cl_firesim/verif/usp_pci_exp_usrapp_tx.v`
- `platforms/xilinx_alveo_v80/cl_firesim/verif/tests.vh`
