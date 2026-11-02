# V80 Metasimulation - Bare Hello Workload

## Date: 2026-08-04

## Summary
Successfully ran Verilator metasimulation of the bare `hello` workload on the V80 platform (FireSimRocket8GiBDRAMConfig).

## Key Findings

### 1. Hello binary needed compilation
The bare hello binary at `/home/ray/chipyard/software/firemarshal/test/bare/hello` did not exist pre-built.
- Built from source using `make` in the test/bare directory
- Had to build in /tmp/bare_build/ due to permission issues in the source directory
- Uses riscv64-unknown-elf-gcc cross-compiler

### 2. UART vs HTIF output path
The bare workload uses HTIF (Host-Target Interface) for `printf` output, NOT the UART bridge.
- `uart.cc` UART bridge has three modes: stdin/stdout (UART0 default), PTY (UART>0), file (+uart-in0/+uart-out0)
- The `+uart-out0=uartlog` flag only captures UART bridge output, not HTIF output
- HTIF output goes to stdout, captured by fesvr
- FireSim deploy uses `script -f -c '<cmd>' uartlog` to capture stdout to uartlog file
- For metasim: stdout contains "Hello World" (HTIF), stderr contains commit trace + PASSED/performance

### 3. stdout vs stderr separation
- **stdout**: simulation init messages, UART0 status, TracerV config, tsibridge ticks, "Hello World"
- **stderr**: commit trace (C0: ... pc=[...]), "Simulation complete", "*** PASSED ***", performance summary

### 4. Simulation results
- Completed in ~3.5 seconds wallclock time
- 9730 target cycles emulated
- FMR: 1.51 (host cycles per target cycle)
- Exit code: 0

## Verification Results
1. ✓ uartlog contains 'Hello World'
2. ✓ No FASED errors or assertion failures  
3. ✓ Simulation completed normally (*** PASSED *** after 9730 cycles)
4. ✓ Exit code 0

## Files
- GEN_DIR: $FIRESIM/sim/generated-src/xilinx_alveo_v80/xilinx_alveo_v80-firesim-FireSim-FireSimRocket8GiBDRAMConfig-BaseXilinxAlveoV80Config
- Binary: /tmp/bare_build/hello (compiled from $CHIPYARD/software/firemarshal/test/bare/)
- Output: $GEN_DIR/uartlog, $GEN_DIR/metasim.log
