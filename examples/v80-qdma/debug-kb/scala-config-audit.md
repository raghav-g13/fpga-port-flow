# Scala Config Audit - Part 1 (2026-08-04)

## Changes Made to Config.scala

### Issue 1: V80 DDR4 capacity was wrong
- **File**: `$FIRESIM/sim/midas/src/main/scala/midas/Config.scala`
- **Problem**: XilinxAlveoV80Config had `size = 0x200000000L` (8 GiB), but V80 has 32 GiB DDR4
- **Fix**: Changed to `size = 0x800000000L` (32 GiB)

### Issue 2: F1Config CPUManagedAXI4Key idBits was globally changed to 16
- **Problem**: F1Config's CPUManagedAXI4Key had `idBits = 16` (was changed from 6 during V80 work). This is a V80-specific need and breaks F1 platform.
- **Fix**: Reverted F1Config back to `idBits = 6`. Removed stale `// idBits = 6,` comment.

### Issue 3: V80 needed its own CPUManagedAXI4Key override
- **Problem**: V80 needs `idBits = 16` for CPUManagedAXI4Key, but this was being applied globally via F1Config.
- **Fix**: Added explicit `CPUManagedAXI4Key` override in XilinxAlveoV80Config with `idBits = 16`, `addrBits = 64`, `dataBits = 512`.

### Build Result
- `sbt 'project midas' compile` succeeded (194s)
- Warnings only (match exhaustiveness, feature flags) - no errors
