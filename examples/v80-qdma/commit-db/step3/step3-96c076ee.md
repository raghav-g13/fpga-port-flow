---
step: 3
id: step3-96c076ee
status: active
created: 2026-08-05T01:29:01.782126+00:00
---

# Step 3 checkpoint

## Commit sequence

1. `FIRESIM-STEP3-PART1-ITER2`
2. `CHIPYARD-STEP3-PART1-ITER2`
3. `FIRESIM-STEP3-PART2-ITER2`
4. `CHIPYARD-STEP3-PART2-ITER2`

## Verification

Part 1: ["Verified Change A: H2C descriptor address byte at DATA_STORE[H2C_ADDR+(k*32)+20] correctly guarded with `ifdef FIRESIM_EP`, changing 8'h01→8'h03 (line 8298-8302). With byte [21]=8'h02, the full card-side address becomes 0x0203_0000_0000", "Verified Change B: C2H descriptor address byte at DATA_STORE[C2H_ADDR+(k*32)+4] correctly guarded with `ifdef FIRESIM_EP`, changing 8'h01→8'h03 (line 8354-8358). With byte [5]=8'h02, the full card-side address becomes 0x0203_0000_0000", "Verified Change C: run_vcs.sh update_simulate_do() writes 'run 20ms' (exceeds the 5ms minimum in criteria, provides margin for full DMA round-trip)", "Verified ifdef/else/endif blocks are syntactically balanced and preserve original values (8'h01) for non-FireSim builds", 'Verified NoC routing via nocattrs.dat: S00_AXI_nmu MADDR1=0x02030000 → DST1=0xC0 → M00_AXI_nsu (REG_SRC=0xC0) which connects to PCIE_M_AXI (512-bit DMA port → F1Shim io_pcis). The old address 0x0201 would route via MADDR0/DST0=0x40 to M01_AXI_nsu (BAR/LITE port), confirming the fix is correct', 'Verified +define+FIRESIM_EP= is passed to all vlogan compile commands in board.sh', 'Verified VCS compile log shows usp_pci_exp_usrapp_tx.v was parsed without errors', 'Verified VCS elaborate log shows pci_exp_usrapp_tx module was recompiled and board_simv binary (4.98MB) was produced successfully with no errors (546s compile + 57s elab + 6s link)', "Verified no compilation errors in compile.log, compile_full.log, or elaborate.log (only 'Error' matches are module names: ErrorDeviceWrapper, NastiErrorSlave)", 'Confirmed existing simulate.log shows test started correctly (qdma_mm_firesim_test0, H2C DMA initiated) but ran out of time at 5ms — the 20ms timeout change addresses this']
Part 2: ['Verified overall_fpga_top.v exists with simulation-only AXI SRAM gated by `ifdef SIMULATION` (8KB SRAM with write/read FSMs and proper AXI4 handshaking)', 'Verified the `else` branch preserves original F1Shim direct connections for synthesis path — no synthesis impact', 'Verified run_vcs.sh includes overall_fpga_top.v in needs_recompile() check list', 'Confirmed build order: overall_fpga_top.v (17:53) → board_simv recompiled (18:14) → simulation ran (18:20) — all Aug 4', 'Found simulate_full.log in $CL_DIR/vcs/vcs/ (not ced_pcie0/) with correct timestamp Aug 4 18:20', "Milestone 1: 'CDO programming done on both EP and RP' at 46559 ns — PRESENT", "Milestone 2: 'SYSTEM CHECK PASSED' at 77324 ns — PRESENT", "Milestone 3: 'AXI-MM H2C Tests start' → 'AXI-MM H2C Completed' (no timeout) — PRESENT", "Milestone 4: 'AXI-MM C2H Tests start' → 'C2H Transfer Data MATCHES' → 'AXI-MM C2H Completed' (no timeout, data matches) — PRESENT", "Milestone 5: 'qdma_mm_firesim_test0 PASSED' at 141229 ns — PRESENT", 'Simulation reached $finish at 141230 ns, called from tests_firesim.vh line 108', "Command line confirms correct test: '+TESTNAME=qdma_mm_firesim_test0'", 'No ERROR or FAILED lines in simulation log (excluding benign SecureIP contention)', '48 contention warnings all from SIP_CPM5_INST.BUT.PROTECTED (SecureIP — expected and benign)', 'Zero compile errors in compile_full.log', 'tests_firesim.vh properly included via tests.vh → usp_pci_exp_usrapp_tx.v include chain']

## Notes


