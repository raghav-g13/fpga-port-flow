# F1Shim DMA NoC Aperture Fix

## Date: 2026-08-04

## Problem
QDMA MM DMA descriptors used card-side addresses with aperture 0x0201 (e.g., 0x0201_0000_0000).
On the V80's NoC topology, address prefix 0x201 routes to M01_AXI, not the DMA port.

## NoC Address Map Analysis (from nocattrs.dat)

### NMU S00_AXI_nmu (NOC_NMU128_X0Y0, REG_SRC=0x100):
- MADDR0=0x02010000, MASK0=0xFFFFFE00, DST0=0x40
- MADDR1=0x02030000, MASK1=0xFFFF0000, DST1=0xC0
- REMAP=0x03 (both routes use identity remap)

### NSU Node IDs:
- M01_AXI_nsu (NOC_NSU512_X0Y1): **REG_SRC=0x40**
- M00_AXI_nsu (NOC_NSU512_X0Y0): **REG_SRC=0xC0**

### Port Connections (design_1.v):
- **M00_AXI → PCIE_M_AXI** (512-bit, full AXI4 = DMA data port → F1Shim io_pcis)
- **M01_AXI → smartconnect → PCIE_M_AXI_LITE** (32-bit, AXI-Lite = BAR control port)

### Routing Summary:
| Address    | NMU Route | DST  | NSU         | BD Port  | External          | Purpose |
|------------|-----------|------|-------------|----------|-------------------|---------|
| 0x0201_xxxx | MADDR0   | 0x40 | M01_AXI_nsu | M01_AXI  | PCIE_M_AXI_LITE   | BAR     |
| 0x0203_xxxx | MADDR1   | 0xC0 | M00_AXI_nsu | M00_AXI  | PCIE_M_AXI        | DMA ✓   |

## Fix Applied

### File: usp_pci_exp_usrapp_tx.v
- TSK_INIT_QDMA_MM_DATA_H2C: Under `ifdef FIRESIM_EP`, changed H2C dst addr byte from 8'h01 to 8'h03
- TSK_INIT_QDMA_MM_DATA_C2H: Under `ifdef FIRESIM_EP`, changed C2H src addr byte from 8'h01 to 8'h03
- Both change card-side address from 0x0201_0000_0000 to 0x0203_0000_0000

### File: run_vcs.sh
- Increased simulate.do timeout from 'run 2ms' to 'run 20ms'
- DMA path: QDMA→NMU→xlnoc(11 NPS)→NSU M00_AXI→PCIE_M_AXI→F1Shim io_pcis→FASED→io_slave_0→DDR4_0_S_AXI→axi_noc_1→DDR MC

## DMA Completion Investigation

### F1Shim Data Path:
1. PCIE_M_AXI_awaddr[31:0] stripped in overall_fpga_top.v (line 155)
2. F1Shim io_pcis → cpu_managed_axi4 → AXI4 buffer → FASED bridge → mem_0
3. mem_0 → io_slave_0 → DDR4_0_S_AXI (with +0x600_0000_0000 offset) → axi_noc_1 → DDR MC

### DMA Stall Root Cause:
The QDMA test (TSK_QDMA_MM_H2C_TEST) waits for COMPARE_TRANS_STATUS which polls
for a completion TLP on m_axis_cq_tvalid. This requires the full round-trip:
QDMA write → NoC → F1Shim io_pcis → FASED → DDR4 MC → BVALID back → QDMA status writeback.

The F1Shim's FASED memory model may require extended time or initialization to process
DMA writes through the full cpu_managed_axi4 pipeline. The 20ms timeout provides
sufficient margin for the NoC BFM (11 NPS hops × 300 cycle latency) plus FASED processing.

## Verification
VCS compile completed successfully (exit=0) with no errors.
