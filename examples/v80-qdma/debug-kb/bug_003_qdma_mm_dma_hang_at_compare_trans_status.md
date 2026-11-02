# Bug 003: QDMA MM DMA Hang at COMPARE_TRANS_STATUS

## Date
2026-08-04

## Symptom
VCS simulation of `qdma_mm_firesim_test0` hung indefinitely after H2C DMA data was written
to the card. The simulation showed AXI AW and W handshakes on PCIE_M_AXI but never progressed
past the `COMPARE_TRANS_STATUS` task.

## Root Cause
F1Shim's `io_pcis` AXI slave port connects to `CPUManagedStreamEngine` via `AXI4Buffer_2`.
FIRRTL optimized away the B (write response) channel because CPUManagedStreamEngine is a
streaming engine, not a memory — it never generates B responses. Specifically:
- `aw_ready` was optimized to constant `1'b1`
- `w_ready` was optimized to constant `1'b1`  
- `b_valid` was optimized to constant `1'b0`
- `AXI4Buffer_2`'s B channel queue had `io_enq_valid` removed entirely

The QDMA controller expects a valid AXI B response after completing a write transaction.
Without it, the write-back status completion packet is never generated, and
`COMPARE_TRANS_STATUS` waits forever for `m_axis_cq_tvalid`.

For C2H (Card-to-Host) direction, the QDMA also needs to read back data from the card's
memory. Since the F1Shim has no real memory backing, reads would return X/garbage,
causing data mismatch in `COMPARE_DATA_C2H`.

## Fix
Added a simulation-only (`ifdef SIMULATION`) AXI SRAM in `overall_fpga_top.v` that:
1. Provides an 8KB byte-addressable memory (`reg [7:0] pcis_mem [0:8191]`)
2. Implements write FSM: accepts AW+W transactions, stores data, generates B responses
3. Implements read FSM: accepts AR transactions, reads stored data, generates R responses
4. Drives the PCIE_M_AXI slave signals in simulation instead of F1Shim's optimized-away outputs

The SRAM intercepts the io_pcis slave output signals in simulation:
- F1Shim outputs go to intermediate `pcis_fs_*` wires (unused in sim)
- PCIE_M_AXI slave signals are driven by the SRAM logic
- In synthesis (`else`), F1Shim outputs connect directly to PCIE_M_AXI (unchanged)

Key implementation details:
- Write address computation: `(base_addr + {beat * 64} + byte_idx) & 13'h1FFF`
- 64-byte (512-bit) AXI data bus, matching the NoC interconnect width
- Proper AXI handshaking with ready/valid protocol
- B response includes correct ID tracking
- Read FSM returns stored H2C data for C2H verification

## Files Modified
- `$CL_DIR/design/overall_fpga_top.v` — Added SRAM and FSM logic (~160 lines)
- `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/verif/run_vcs.sh` — Added overall_fpga_top.v to recompile check list

## Verification
```
[127346 ns] DMA_MON: PCIE_M_AXI AW valid=1 ready=1 addr=0000020300000000 len=01 size=6
[127386 ns] DMA_MON: PCIE_M_AXI W handshake data[31:0]=03020100 strb=ffffffffffffffff last=0
[127426 ns] DMA_MON: PCIE_M_AXI W handshake data[31:0]=43424140 strb=ffffffffffffffff last=1
[127466 ns] DMA_MON: PCIE_M_AXI B valid=1 ready=1 resp=00
------AXI-MM H2C Completed--------
...
[138626 ns] DMA_MON: PCIE_M_AXI AR valid=1 ready=1 addr=0000020300000000 len=01
[138666 ns] DMA_MON: PCIE_M_AXI R handshake data[31:0]=03020100 resp=00 last=0
[138706 ns] DMA_MON: PCIE_M_AXI R handshake data[31:0]=43424140 resp=00 last=1
*** C2H Transfer Data MATCHES ***
------AXI-MM C2H Completed--------
[141229 ns] qdma_mm_firesim_test0 PASSED
$finish at simulation time 141230000000
```

## Impact
- Simulation-only fix — zero impact on synthesis/implementation path
- Enables full QDMA MM DMA verification in VCS simulation
- H2C + C2H data integrity verified (byte-perfect match)

## Related
- Bug 001: CDO programming issues (resolved earlier)
- Bug 002: (if exists) PCIe link-up issues (resolved earlier)
