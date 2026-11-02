# XDMA BAR sizing mismatch on V80

## Classification

- **Category**: fpga
- **Target**: XilinxAlveoV80
- **Porting step**: 3
- **Severity**: blocker
- **Status**: resolved

## Environment

- **FireSim commit/version**: main
- **Tool version**: Vivado 2025.1

## Trigger

```bash
cd $FIRESIM && source sourceme-manager.sh
firesim buildbitstream
```

## Error

```
ERROR: [DRC RPBF-3] IO buffer overutilization: BAR0 size (64M) exceeds
available PCIe aperture on V80 (32M for XDMA config).
```

## Root cause

The V80 XDMA IP defaults to 32M BAR0 aperture, but FireSim's DMA engine
assumes 64M (inherited from U250 config). The BAR size is set in the XDMA IP
properties and must match the FireSim driver's expected mapping.

## Resolution

Set BAR0 to 32M in the XDMA IP config and update the FireSim driver's
`MMIO_BAR_SIZE` constant to match.

### Files modified

- `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/scripts/create_bd.tcl`: Set `CONFIG.pf0_bar0_size` to `32M`
- `$FIRESIM/sim/firesim-lib/src/main/cc/bridges/xdma/xdma_driver.h`: `MMIO_BAR_SIZE = 0x2000000`

## Related

- See `tools/vivado/drc-rpbf3-false-positive.md` for cases where this DRC fires spuriously
