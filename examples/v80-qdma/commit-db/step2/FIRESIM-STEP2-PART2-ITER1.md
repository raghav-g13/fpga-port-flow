---
id: FIRESIM-STEP2-PART2-ITER1
repo: FIRESIM
step: 2
part: 2
iter: 1
parent: CHIPYARD-STEP2-PART1-ITER3
timestamp: 2026-08-04T19:03:32.517508+00:00
git_hash: STDERR:
---

# step2/part2: Fixed NoC NMU address decode in nocattrs.dat to route CPM5 BAR2 traffic (addr 0x020180000224) to PCIE_M_AXI_LITE NSU. Added MADDR2=0x02018000 with RPADDR2=0x02010000 to remap the address into the Smar

## Message

Fixed NoC NMU address decode in nocattrs.dat to route CPM5 BAR2 traffic (addr 0x020180000224) to PCIE_M_AXI_LITE NSU. Added MADDR2=0x02018000 with RPADDR2=0x02010000 to remap the address into the SmartConnect's 32MB segment at 0x020100000000. Enabled region 2 in REG_ADDR_ENABLE and REG_ADDR_REMAP. Two bugs were fixed: (1) NMU $fatal due to missing address decode entry for BAR2 output addresses, and (2) SmartConnect DECERR (0xdec0dee3) due to identity RPADDR not remapping into the valid segment range.

## Diff

```diff

STDERR:
error: Could not access 'STDERR:'

[exit code: 1]
```

## Files modified

- `platforms/xilinx_alveo_v80/cl_xilinx_alveo_v80-firesim-FireSim-FireSimRocket8GiBDRAMConfig-BaseXilinxAlveoV80Config/vcs/vcs/nocattrs.dat`
