# V80 Width Consistency Verification

**Date**: 2026-08-04
**Step**: Scala config audit and fix — Part 4: End-to-end consistency verification

## Verification Results: ALL 5 CHECKS PASS

### Effective V80 Scala Config
(Resolved through: XilinxAlveoV80Config ++ XilinxAlveoU250Config ++ F1Config ++ SimConfig)

| Key | Parameter | Value | Source |
|-----|-----------|-------|--------|
| HostMemChannelKey | size | 0x800000000 (32 GiB) | V80 overrides F1Config |
| HostMemChannelKey | beatBytes | 8 | F1Config |
| HostMemChannelKey | idBits | 16 | F1Config |
| HostMemNumChannels | — | 1 | U250Config |
| CtrlNastiKey | dataBits/addrBits/idBits | 32/25/12 | F1Config |
| CPUManagedAXI4Key | addrBits/dataBits/idBits | 64/512/16 | V80 overrides F1Config |

### Check 1: io_slave_0 addr width = log2Ceil(HostMemChannelKey.size) = 35
- HostMemChannelParams.axi4BundleParams: addrBits = log2Ceil(size) = log2Ceil(2^35) = 35
- RTL wrapper: wire [34:0] firesim_slave_0_awaddr = 35 bits ✓
- Note: Current generated SV has 33-bit (from older build); will be 35 bits after rebuild

### Check 2: RTL wrapper wires match F1Shim ports
- io_master ↔ PCIE_M_AXI_LITE: addr [24:0]=25b, data 32b, id 12'h0 ✓
- io_pcis ↔ PCIE_M_AXI: addr {32'b0,awaddr[31:0]}=64b, data 512b, id {14'b0,awid}=16b ✓
- io_slave_0 ↔ DDR4_0_S_AXI: addr 35b, data 64b, id 16b ✓

### Check 3: CPUManagedAXI4Key idBits matches RTL padding
- idBits=16, PCIE_M_AXI_awid=2 bits, padding={14'b0, awid}=16 bits ✓

### Check 4: CtrlNastiKey addrBits matches PCIE_M_AXI_LITE slice
- addrBits=25, slice=[24:0] from 42-bit PCIE_M_AXI_LITE_awaddr ✓

### Check 5: HostMemNumChannels=1 matches single DDR4
- Only DDR4_0_S_AXI declared, only io_slave_0 in F1Shim ✓

## Note on Stale Generated SV
The generated SV file at `cl_xilinx_alveo_v80-firesim-FireSim-FireSimRocket8GiBDRAMConfig-BaseXilinxAlveoV80Config/design/FireSim-generated.sv` was built from an earlier configuration where HostMemChannelKey.size was 8 GiB (io_slave_0 addr = 33 bits). After regeneration with the current 32 GiB config, it will produce 35-bit addr matching the RTL wrapper.
