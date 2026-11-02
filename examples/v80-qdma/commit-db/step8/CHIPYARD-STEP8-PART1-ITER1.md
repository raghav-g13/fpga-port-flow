---
id: CHIPYARD-STEP8-PART1-ITER1
repo: CHIPYARD
step: 8
part: 1
iter: 1
parent: FIRESIM-STEP8-PART1-ITER1
timestamp: 2026-08-05T08:00:03.666738+00:00
git_hash: STDERR:
---

# step8/part1: Created $FIRESIM/platforms/xilinx_alveo_v80/scripts/ directory and copied all 10 deploy scripts from the U250 platform (xilinx_alveo_u250/scripts/) preserving file permissions. These scripts handle PC

## Message

Created $FIRESIM/platforms/xilinx_alveo_v80/scripts/ directory and copied all 10 deploy scripts from the U250 platform (xilinx_alveo_u250/scripts/) preserving file permissions. These scripts handle PCIe disconnect/reconnect (firesim-fpga-util.py, pcielib.py), JTAG programming (program_fpga_fleet.tcl, program_fpga.tcl, program_fpga_all.tcl), FPGA DB generation (firesim-generate-fpga-db.py), Vivado helpers (util.py), serial device discovery (get_serial_dev_for_fpgas.tcl), flash programming (program_flash.tcl), and Berkeley FPGA setup (berkeley-setup-fpgas.sh). The program_fpga_fleet.tcl already supports PDI files via program_hw_devices.

## Diff

```diff

STDERR:
error: Could not access 'STDERR:'

[exit code: 1]
```

## Files modified

- `$FIRESIM/platforms/xilinx_alveo_v80/scripts/pcielib.py`
- `$FIRESIM/platforms/xilinx_alveo_v80/scripts/util.py`
- `$FIRESIM/platforms/xilinx_alveo_v80/scripts/firesim-fpga-util.py`
- `$FIRESIM/platforms/xilinx_alveo_v80/scripts/firesim-generate-fpga-db.py`
- `$FIRESIM/platforms/xilinx_alveo_v80/scripts/program_fpga_fleet.tcl`
- `$FIRESIM/platforms/xilinx_alveo_v80/scripts/get_serial_dev_for_fpgas.tcl`
- `$FIRESIM/platforms/xilinx_alveo_v80/scripts/program_fpga.tcl`
- `$FIRESIM/platforms/xilinx_alveo_v80/scripts/program_fpga_all.tcl`
- `$FIRESIM/platforms/xilinx_alveo_v80/scripts/program_flash.tcl`
- `$FIRESIM/platforms/xilinx_alveo_v80/scripts/berkeley-setup-fpgas.sh`
