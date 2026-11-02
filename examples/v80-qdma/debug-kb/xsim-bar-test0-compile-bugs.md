# XSim bar_test0 Compile Bugs

## Bug 1: `$isunknown` not allowed in Verilog dialect

**File**: `cl_firesim/verif/tests_firesim.vh`  
**Error**: `[VRFC 10-9406] system call 'isunknown' is not allowed in this dialect; use SystemVerilog mode instead`

**Root cause**: `tests_firesim.vh` is included by `usp_pci_exp_usrapp_tx.v` (a `.v` file), so XSim compiles it in Verilog-2001 mode. `$isunknown()` is a SystemVerilog-only system function.

**Fix**: Replace `$isunknown(val)` with the Verilog-compatible idiom `(^val === 1'bx)`.  
XOR of all bits propagates any X/Z to the result; `=== 1'bx` checks for exact X match.

```diff
- if ($isunknown(board.RP.tx_usrapp.P_READ_DATA)) begin
+ if ((^board.RP.tx_usrapp.P_READ_DATA === 1'bx)) begin
```

Applied at 4 locations (one per register read step in bar_test0).

## Bug 2: Locale crash — `en_US.UTF-8` not available

**Error**: `terminate called after throwing an instance of 'std::runtime_error'` / `locale::facet::_S_create_c_locale name not valid`

**Root cause**: Vivado 2025.1's `rdiArgs.sh` (line 37) hardcodes `export LC_ALL="en_US.UTF-8"`. In Docker containers without the `locales` package, this locale doesn't exist, causing the xvlog/xelab/xsim binaries to abort.

**Fix**: Create a symlink-based locale entry before invoking Vivado tools:
```bash
mkdir -p /tmp/mylocale
ln -sf /usr/lib/locale/C.utf8 /tmp/mylocale/en_US.UTF-8
export LOCPATH=/tmp/mylocale:/usr/lib/locale
```

This makes `en_US.UTF-8` resolve to `C.utf8` (the only UTF-8 locale available in the container). Added to `run_xsim.sh` as an automatic patch.

## Bug 3: xlnoc module not found during elaboration

**Error**: `[VRFC 10-2063] Module <xlnoc> not found while processing module instance <xlnoc_i>`

**Root cause**: The `board_firesim.v` testbench instantiates `xlnoc` (the NoC fabric BFM), but the xlnoc source files were not included in `vlog.prj`. The vlog.prj only had include paths to the xlnoc ipshared BFM directory, not the actual xlnoc source files for compilation.

**Fix**: Added the following to `vlog.prj` (before `board_firesim.v`):
1. `noc_nps_v1_0_vl_rfs.sv` — NPS BFM library (SystemVerilog)
2. `xlnoc_nps_X_0.sv` and `xlnoc_nps_X_0_top.sv` for X in 0-10 — NPS instance wrappers
3. `xlnoc.v` (sim version) — BD simulation netlist

**Note**: Do NOT add `nps_class_new.sv`, `nps_ipa.sv`, `nps_ivca.sv`, `nps_load_parameters.sv` individually — they're already compiled within `noc_nps_v1_0_vl_rfs.sv` and cause "already declared" errors if compiled separately.

The xlnoc BD has 11 NPS (Network Packet Switch) instances that model the NoC routing fabric. Without these, the NMU and NSU BFM ports are unconnected ('x values on noc_valid and noc_credit_return).
