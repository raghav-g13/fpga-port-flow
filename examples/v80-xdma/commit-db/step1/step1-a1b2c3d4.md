---
step: 1
id: step1-a1b2c3d4
status: active
created: 2026-01-15T12:00:00Z
---

# Step 1 checkpoint: V80 XDMA platform scaffolding

## Commit sequence

1. `FIRESIM-STEP1-PART1-ITER1`

## Verification

- `ls -R $FIRESIM/platforms/xilinx_alveo_v80/` shows expected directory structure
- Vivado TCL sources without syntax errors: `vivado -mode batch -source create_bd.tcl -notrace`

## Notes

Initial scaffolding for V80 XDMA platform. Adapted from U250 XDMA shell.
