---
id: FIRESIM-STEP4-PART3-ITER1
repo: FIRESIM
step: 4
part: 3
iter: 1
parent: CHIPYARD-STEP4-PART2-ITER1
timestamp: 2026-08-05T04:31:08.576892+00:00
git_hash: STDERR:
---

# step4/part3: Updated RTL wrapper wire widths and padding in both overall_fpga_top.v files to match regenerated F1Shim port widths. (1) Changed firesim_slave_0_awaddr/araddr wire declarations from [39:0] (40 bits) 

## Message

Updated RTL wrapper wire widths and padding in both overall_fpga_top.v files to match regenerated F1Shim port widths. (1) Changed firesim_slave_0_awaddr/araddr wire declarations from [39:0] (40 bits) to [34:0] (35 bits) to match F1Shim io_slave_0_aw/ar_bits_addr [34:0]. (2) Adjusted zero-padding in assign statements from {24'b0, addr} to {29'b0, addr} so concatenation totals 64 bits (29+35=64) matching DDR4_0_S_AXI 64-bit address bus. (3) In the config copy's SIMULATION block, fixed pcis_fs_bid and pcis_fs_rid intermediate wire widths from [1:0] to [15:0] to match F1Shim io_pcis_b/r_bits_id [15:0]. All slave_0 ID wires (DDR4_0_S_AXI_awid etc.) already matched F1Shim's [15:0] via the AMBA_AXI_WIRE macro with 16-bit ID parameter.

## Diff

```diff

STDERR:
error: Could not access 'STDERR:'

[exit code: 1]
```

## Files modified

- `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/design/overall_fpga_top.v`
- `$FIRESIM/platforms/xilinx_alveo_v80/cl_xilinx_alveo_v80-firesim-FireSim-FireSimRocket8GiBDRAMConfig-BaseXilinxAlveoV80Config/design/overall_fpga_top.v`
