# Part 3: RTL Wire Width Alignment

## Date: 2026-08-04

## Issue
The `firesim_slave_0_awaddr` and `firesim_slave_0_araddr` intermediate wires in `overall_fpga_top.v` were declared as `[39:0]` (40 bits), but the regenerated F1Shim has `io_slave_0_aw_bits_addr [34:0]` and `io_slave_0_ar_bits_addr [34:0]` (35 bits each). This created a 5-bit width mismatch.

Additionally, in the config copy's SIMULATION block, `pcis_fs_bid` and `pcis_fs_rid` were declared as `[1:0]` (2 bits) but F1Shim's `io_pcis_b_bits_id` and `io_pcis_r_bits_id` are `[15:0]` (16 bits).

## Root Cause
The original wire widths were set based on an older F1Shim configuration (possibly 40-bit address from a different Scala config). After Part 2 regenerated the F1Shim with updated Scala configs, the address width became 35 bits (matching `HasDRAMChannel` with `memAddrBits=35`).

## Fix
1. Changed `wire [39:0] firesim_slave_0_awaddr` → `wire [34:0] firesim_slave_0_awaddr`
2. Changed `wire [39:0] firesim_slave_0_araddr` → `wire [34:0] firesim_slave_0_araddr`
3. Changed padding from `{24'b0, addr}` to `{29'b0, addr}` (29+35=64 bits for DDR4 AXI 64-bit address)
4. Changed `pcis_fs_bid` from `[1:0]` to `[15:0]` (matches F1Shim io_pcis_b_bits_id)
5. Changed `pcis_fs_rid` from `[1:0]` to `[15:0]` (matches F1Shim io_pcis_r_bits_id)

## Files Modified
- `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/design/overall_fpga_top.v`
- `$FIRESIM/platforms/xilinx_alveo_v80/cl_xilinx_alveo_v80-firesim-FireSim-FireSimRocket8GiBDRAMConfig-BaseXilinxAlveoV80Config/design/overall_fpga_top.v`

## Verification
- Wire [34:0] = 35 bits matches F1Shim io_slave_0_aw_bits_addr [34:0]
- {29'b0, 35-bit} = 64 bits matches DDR4_0_S_AXI 64-bit address
- F1Shim io_slave_0_aw_bits_id [15:0] connects directly to DDR4_0_S_AXI_awid [15:0] - no change needed
- pcis_fs_bid/rid [15:0] matches F1Shim io_pcis_b/r_bits_id [15:0]
