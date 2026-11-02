# Bug 010: add_line_to_file TCL procedure crash

## Symptom
`firesim buildbitstream` fails during Vivado project creation with TCL error:
```
can't read "result": no such variable
    while executing
"puts "ERROR: Updating ${ifile} failed ($result)""
    (procedure "add_line_to_file" line 2)
```

## Root Cause
The `add_line_to_file` procedure in `scripts/utils.tcl` uses `catch` without capturing the result variable:
```tcl
if {[catch {exec sed -i "${lineno}i ${istr}\\n" ${ifile}}]} {
    puts "ERROR: Updating ${ifile} failed ($result)"   ;# $result not defined!
    exit 1
}
```

The `catch` should be `catch {...} result` to capture the error message. Additionally, the `exec sed` command fails because the sed pattern contains special characters (brackets from `[get_cells ...]`) and the `\\n` literal.

## Fix
1. Fixed `catch` to capture result: `catch {...} result`
2. Made the procedure robust: on sed failure, fall back to Tcl file I/O
3. Changed `exit 1` to `puts WARNING` — this line insertion is a URAM optimization hint, not critical for build correctness

## Files Modified
- `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/scripts/utils.tcl` (template)
- `$FIRESIM/platforms/xilinx_alveo_v80/cl_<quintuplet>/scripts/utils.tcl` (build copy)
