---
step: 2
id: step2-b4dcce01
status: active
created: 2026-08-04T19:03:32.527981+00:00
---

# Step 2 checkpoint

## Commit sequence

1. `FIRESIM-STEP2-PART1-ITER3`
2. `CHIPYARD-STEP2-PART1-ITER3`
3. `FIRESIM-STEP2-PART2-ITER1`
4. `CHIPYARD-STEP2-PART2-ITER1`

## Verification

Part 1: ["bar_test0 else-if block exists in tests_firesim.vh at line 7, keyed on testname=='bar_test0'", 'bar_test0 is placed BEFORE qdma_mm_firesim_test0 (line 7 vs line 88)', "Include chain verified: usp_pci_exp_usrapp_tx.v if(dummy_test) → include tests.vh → include tests_firesim.vh → else-if chain terminates with fallback 'Unrecognized TESTNAME' — bar_test0's else-if chains correctly", "Step 1: Reads PRESENCE_READ at offset 0x224 via TSK_REG_READ(user_bar, 16'h224), verifies == 0x46697265", "Step 2: Reads INIT_DONE at offset 0x220 via TSK_REG_READ(user_bar, 16'h220), verifies == 32'h1", "Step 3: Writes 0xDEADBEEF to PRESENCE_WRITE at 0x228 via TSK_REG_WRITE(user_bar, 32'h228, 32'hDEADBEEF, 4'hF), then reads back PRESENCE_READ at 0x224 and verifies == 0xDEADBEEF", "Step 4: Reads PeekPoke DONE at offset 0x1D0 via TSK_REG_READ(user_bar, 16'h1D0), checks for non-X", 'All register offsets match reference: INIT_DONE=0x220, PRESENCE_READ=0x224, PRESENCE_WRITE=0x228, PeekPoke DONE=0x1D0', "TSK_REG_READ argument types match task signature: (integer bar_num, [15:0] read_addr) — test passes (user_bar, 16'hXXX)", "TSK_REG_WRITE argument types match task signature: (integer bar_num, [31:0] addr, [31:0] data, [3:0] byte_en) — test passes (user_bar, 32'h228, 32'hDEADBEEF, 4'hF)", "X-value checking on all 4 reads using (^P_READ_DATA === 1'bx) — Verilog-compatible equivalent of $isunknown()", 'Failures tracked via board.RP.tx_usrapp.test_state = 1', 'Test reports PASSED/FAILED based on test_state and calls $finish', 'TSK_PROG_HOST_PROFILE called at start to initialize BARs (user_bar set to correct value)', 'begin/end balance verified: 14 begins, 3 outer ends matching 3 test blocks, inner ends properly paired']
Part 2: ['Confirmed bar_test0 test case exists in tests_firesim.vh (line 7)', 'Confirmed nocattrs.dat changes: MADDR2=0x02018000, RPADDR2=0x02010000, REG_ADDR_ENABLE=0x00000007, REG_ADDR_REMAP=0x00000007 on S00_AXI_nmu of axi_noc_0', 'Ran VCS simulation: cd cl_firesim/verif && bash run_vcs.sh simulate +TESTNAME=bar_test0 (recompile, re-elaborate, simulate)', 'CDO programming done: [46559 ns] CDO programming done on both EP and RP', 'PCIe link-up achieved: [76559 ns] user_lnk_up=1 ltssm=10 (maintained throughout simulation)', 'BAR enumeration completed: BAR 0 (MEM64) and BAR 2 (MEM64) mapped; SYSTEM CHECK PASSED at 77324 ns', 'MMIO reads return valid data — PRESENCE_READ=0x46697265 (correct FireSim fingerprint), INIT_DONE=0x00000001, write-readback=0xdeadbeef, PeekPoke DONE=0x00000001', 'Test passed: [126197 ns] bar_test0 PASSED', '$finish reached at simulation time 126198000000 fs', "Zero $fatal errors in simulate.log (grep -ci 'fatal' returned 0)", 'No NoC NMU $fatal errors (NMU mentions only from nocattrs.dat updates, not errors)', 'ADEC checks are passing (NoC address decode verified by VCS NoC model)', '85 non-fatal Chisel assertion messages from ctrlInterconnect.xbar.router (benign timing artifacts, not $fatal)', 'Simulation exit code = 0']

## Notes


