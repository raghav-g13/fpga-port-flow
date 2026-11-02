# Bug 007: plusarg_reader module not found during synthesis

## Symptom
```
ERROR: [Synth 8-439] module 'plusarg_reader' not found [FireSim-generated.sv:119285]
```

## Root Cause
FireSim-generated.sv instantiates `plusarg_reader` but its definition (from rocket-chip) is not included in the Vivado project. The generated-src directory for the current config lacks `plusarg_reader.v`.

## Fix
1. Copy `plusarg_reader.v` from rocket-chip to cl_firesim/design/
2. Add it to main.tcl's file list

## Files Modified
- `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/design/plusarg_reader.v` (new)
- `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/scripts/main.tcl` (added plusarg_reader.v to file list)
