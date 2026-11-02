# Verilator Metasimulation Build (VFireSim) - V80 Platform

## Date: 2026-08-04

## Task
Build VFireSim (Verilator metasimulation model) from Golden Gate output for Xilinx Alveo V80.

## Key Issue: Missing `plusarg_reader` module
### Symptom
```
%Error: FireSim-generated.sv:119285:3: Cannot find file containing module: 'plusarg_reader'
```

### Root Cause
Golden Gate generates `plusarg_reader.v` and `AbstractClockGate.v` as separate black box files in `$GEN_DIR`.
The inner Makefile (`$FIRESIM/sim/midas/src/main/cc/Makefile`) only includes `FireSim-generated.sv`,
`FireSim-generated.const.vh`, and `BUFGCE.v` as Verilog sources. It does NOT include the black box
resource files.

The outer Makefile's Golden Gate rule (`goldengate.mk`) appends black box contents to the generated .sv
via: `grep -sh ^ $GEN_DIR/firrtl_black_box_resource_files.f | xargs cat >> $simulator_verilog`

But in our flow we skip the outer Makefile and call the inner one directly (to avoid firechip.jar dependency).

### Fix
Add `-y $GEN_DIR` to `VERILATOR_FLAGS` so Verilator searches that directory for missing module definitions:
```
VERILATOR_FLAGS="--assert -y $GEN_DIR"
```

### Alternative Fix (not used)
Could also manually append the black box files before building:
```
grep -sh ^ $GEN_DIR/firrtl_black_box_resource_files.f | xargs cat >> $GEN_DIR/FireSim-generated.sv
```

## Key Variables for Inner Makefile Build

### CXXFLAGS (exported)
```
-isystem $testchipip_csrc_dir -isystem $RISCV/include
-Wno-inconsistent-missing-override
-I$firechip_bridgestubs_lib_dir/bridge/test -I$firechip_bridgestubs_lib_dir
-I$firechip_bridgestubs_lib_dir/bridge -I$firechip_bridgestubs_lib_dir/bridge/tracerv
-I$firechip_bridgestubs_lib_dir/bridge/cospike -I$GEN_DIR
-g -Wno-unused-variable -DFIRESIM -O2 -D RTLSIM
```

### LDFLAGS (exported)
```
-L$RISCV/lib -L$CONDA_PREFIX/lib
-Wl,-rpath,$RISCV/lib -Wl,-rpath,$CONDA_PREFIX/lib
-lriscv -l:libdwarf.so -l:libelf.so -lz -lrt
```

**IMPORTANT**: `libdwarf.so`, `libelf.so`, `libgmp.so` are in `$CONDA_PREFIX/lib` 
(= `$CHIPYARD/.conda-env/lib`), NOT in `$RISCV/lib`. Must add `-L$CONDA_PREFIX/lib`.

### Build Time
~50 seconds (Verilator 5.022, 8-core parallel build, 146K-line SV file)

### Output
VFireSim binary: 47MB ELF 64-bit executable
Location: $GEN_DIR/VFireSim

## Status: SUCCESS
