---
step: 1
id: step1-93fd5ff5
status: active
created: 2026-08-04T10:21:05.267752+00:00
---

# Step 1 checkpoint

## Commit sequence

1. `FIRESIM-STEP1-PART1-ITER1`
2. `CHIPYARD-STEP1-PART1-ITER1`
3. `FIRESIM-STEP1-PART2-ITER1`
4. `CHIPYARD-STEP1-PART2-ITER1`
5. `FIRESIM-STEP1-PART3-ITER1`
6. `CHIPYARD-STEP1-PART3-ITER1`

## Verification

Part 1: ['gen_vcs_firesim.tcl exists (4403 bytes) with correct structure: find_files helper, CL_DIR auto-detect via ../.. (2 levels up from verif/), open_project, PIPESIM patches for EP (design_1) and RP (design_rp), export_simulation -simulator vcs with lib_map_path and -force', 'synopsys_sim.setup has 0 occurrences of /home/ray/chipyard and 42 occurrences of /home/ray/chipyard — paths correctly fixed', 'VCS export directory $CL_DIR/vcs/vcs/ exists and contains board.sh (170163 bytes) plus 30+ supporting files (.cdo, .mem, .dat, .bd, glbl.v, etc.)', 'board.sh is a valid Vivado-generated VCS simulation script using vlogan/vhdlan/vcs commands with correct lib_map_path pointing to vcs_xilinx_lib', 'Vivado journal confirms clean batch execution (vivado -mode batch -stack 2000 -source gen_vcs_firesim.tcl) with no crash or abort', 'Vivado log shows no ERROR lines; only benign HDL 9-3756 WARNINGs (CPM5 interface redefinitions from dual BD), one expected CRITICAL WARNING about cpm5_pipe_sim_wires.vh (EP/RP different configs), and INFO about IPs compiled locally', "Vivado log confirms successful export: 'Script generated: .../vcs/vcs/board.sh' with clean exit at 21:32:23", 'PIPESIM patches verified in .sv source files: EP bd_70da_cpm_0_0.sv has C_CPM_PIPESIM(TRUE)=1, FALSE=0; RP bd_e4ca_cpm_0_0.sv has C_CPM_PIPESIM_CLK_MASTER(TRUE)=1, FALSE=0', 'Script follows patterns from existing setup_xsim.tcl: same argument-handling style, CL_DIR auto-detection, project management, export_simulation call structure']
Part 2: ['run_vcs.sh exists at correct path with executable permissions (755)', 'Script sets VCS_HOME via patched VCS installation (/ecad/tools/synopsys/vcs/W-2024.09-1)', 'Script sets LD_LIBRARY_PATH including lib32/usr/lib/i386-linux-gnu', 'Script sets RDI_DATADIR=/ecad/tools/xilinx/2025.1/data', 'Script sources /ecad/tools/xilinx/2025.1/Vivado/settings64.sh', 'Script accepts CL_DIR as optional arg or auto-detects cl_xilinx_alveo_v80-*', 'Script accepts step argument (compile|elaborate|simulate|all)', 'Script accepts +TESTNAME=... and forwards to simulation', 'board.sh patched: +define+FIRESIM_EP= and +define+SIMULATION= in all 42 vlogan commands', 'board.sh patched: -Xcheck_p1800_2009=char in vlogan_opts', 'board.sh patched: +error+999 -xlrm uniq_prior_final in vcs_elab_opts', 'board.sh patched: synopsys_sim.setup OTHERS path corrected to /home/ray/...', 'usp_pci_exp_usrapp_tx.v: proper ifdef/else/endif guard around COMPARE_DATA_H2C task', 'tests.vh: conditionally excludes sample_tests.vh under FIRESIM_EP, includes tests_firesim.vh', 'tests_firesim.vh exists', 'compile.log: 0 errors, 30 warnings - no ERROR lines', 'elaborate.log: 0 actual errors (false positives from module names), 581 warnings', "elaborate.log confirms 'All of 4194 modules done' and 'board_simv up to date'", 'board_simv binary exists: 4.9MB ELF 64-bit LSB executable, all dynamic deps resolved (ldd clean)']
Part 3: ['Verified run_vcs.sh exists at cl_firesim/verif/run_vcs.sh and accepts +TESTNAME=<value> argument, passing it to board_simv correctly', "Verified VCS compilation completed without errors (0 'Error-' lines in compile_full.log, board_firesim.v parsed successfully)", "Verified VCS elaboration succeeded with board as top module (board_simv binary produced, 4201 modules, elaborate.log confirms 'board_simv up to date')", "Verified simulate.do exists with 'run 2ms; quit' (analogous to CED board_simulate.do)", 'Verified simulation data files present in VCS directory (*.cdo, *.mem, *.csv files all present)', "Verified simulate.log shows correct command line: './board_simv -ucli -licqueue -l simulate.log -do simulate.do +TESTNAME=qdma_mm_test0'", 'Verified CDO programming done on both EP and RP at 46559 ns', 'Verified PCIe link-up: user_lnk_up=1 and LTSSM=0x10 at 76559 ns', 'Verified SYSTEM CHECK PASSED (Link Speed 16.0GT/s, Link Width x8, Device/Vendor ID, CMPS ID)', 'Verified BAR enumeration completed (MEM64 BAR 0 and BAR 2 enabled at 94236 ns)', 'Verified host profile programming completed successfully at 116020 ns', "Verified 'qdma_mm_test0 PASSED' at 116021 ns", 'Verified $finish reached at simulation time 116022000000 fs — clean VCS Simulation Report', 'Verified 0 ERROR or assertion failure lines in simulate_full.log', 'Verified board_firesim.v has only 2 PIPESIM defparams (broken defparams removed per implementation report)', 'Verified modified bd_70da_cpm_0_0.sv and EP CDO file (bd_70da_cpm_0_0_sim.cdo, 91KB) exist']

## Notes


