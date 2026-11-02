# V80 Deploy Manager QDMA Customization - Part 2

## Status: PASS (pre-existing implementation verified correct)

## Methods Verified

### `_compute_qdma_bdf(self, bdf_str)`
- Takes BDF string like 'b1:00.0', splits on ':' and '.'
- Returns `(bus << 12) | (device << 4) | function` as integer
- Matches driver convention in `simif_xilinx_alveo_v80.cc` line 276-278
- Format as `{qdma_bdf:05x}` matches driver's `%05x` (line 282)

### `load_qdma(self)`
- Checks `lsmod | grep -wq qdma_pf` before loading
- Uses `sudo modprobe qdma-pf` to load
- Reads FPGA DB, iterates sim slots
- For each slot: sets qmax via `/sys/bus/pci/devices/0000:{bdf}/qdma/qmax`
- Adds MM queue 0 bidirectional via `dma-ctl`
- Starts MM queue 0 bidirectional via `dma-ctl`
- Sets `/dev/qdma*` permissions to 666

### `unload_qdma(self)`
- Only runs if qdma_pf is loaded
- For each slot: stops and deletes queue 0 with `warn_only` context manager
- Uses `with warn_only():` fabric context manager for graceful failure
- Unloads module with `sudo modprobe -r qdma-pf`

### `flash_fpgas(self)`
- Overrides base class
- Step 1: PCI disconnect all slots via firesim-fpga-util.py
- Step 2: Program all FPGAs via Vivado batch with program_fpga_fleet.tcl
- Step 3: Sleep 10s for PCIe link re-training (Versal PDI resets SoC)
- Step 4: Full PCIe bus rescan via `/sys/bus/pci/rescan` (NOT per-BDF reconnect)
- Step 5: Retry rescan up to 30s (6 iterations * 5s) if devices don't appear
- Step 6: Enable memory-mapped transfers via `setpci -s EBDF COMMAND=0x02`
- Key V80 difference: uses full bus rescan instead of per-BDF reconnect since
  BDF may change after Versal reprogramming

## Validation
- Python AST parse: OK
- All 4 methods present in class: OK
- QDMA BDF computation verified against driver convention: OK
