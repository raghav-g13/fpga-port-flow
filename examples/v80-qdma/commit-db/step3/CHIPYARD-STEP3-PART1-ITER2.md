---
id: CHIPYARD-STEP3-PART1-ITER2
repo: CHIPYARD
step: 3
part: 1
iter: 2
parent: FIRESIM-STEP3-PART1-ITER2
timestamp: 2026-08-04T23:37:09.991716+00:00
git_hash: STDERR:
---

# step3/part1: Three changes implemented and verified: (A) In TSK_INIT_QDMA_MM_DATA_H2C, wrapped DATA_STORE[H2C_ADDR+(k*32)+20] in `ifdef FIRESIM_EP guard, changing 8'h01→8'h03 for H2C destination address 0x0203_000

## Message

Three changes implemented and verified: (A) In TSK_INIT_QDMA_MM_DATA_H2C, wrapped DATA_STORE[H2C_ADDR+(k*32)+20] in `ifdef FIRESIM_EP guard, changing 8'h01→8'h03 for H2C destination address 0x0203_0000_0000. (B) In TSK_INIT_QDMA_MM_DATA_C2H, same guard for DATA_STORE[C2H_ADDR+(k*32)+4] 8'h01→8'h03 for C2H source address. These route through axi_noc_0 MADDR1 (DST1=0xC0) → M00_AXI_nsu (REG_SRC=0xC0) → M00_AXI → PCIE_M_AXI (512-bit DMA port → F1Shim io_pcis), confirmed via nocattrs.dat analysis. (C) In run_vcs.sh update_simulate_do(), increased runtime from 'run 2ms' to 'run 20ms' (up from previous 5ms) to accommodate the full DMA path: QDMA→NMU→xlnoc(11 NPS hops, 300 cycle latency each)→NSU→M00_AXI→F1Shim io_pcis→FASED cpu_managed_axi4→io_slave_0→DDR4_0_S_AXI(+0x600 base)→axi_noc_1→DDR MC BFM. Deep investigation of the DMA stall revealed the COMPARE_TRANS_STATUS task waits for a QDMA completion TLP (m_axis_cq_tvalid) which requires the full round-trip through F1Shim's FASED memory model pipeline.

## Diff

```diff

STDERR:
error: Could not access 'STDERR:'

[exit code: 1]
```

## Files modified

- `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/verif/usp_pci_exp_usrapp_tx.v`
- `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/verif/run_vcs.sh`
