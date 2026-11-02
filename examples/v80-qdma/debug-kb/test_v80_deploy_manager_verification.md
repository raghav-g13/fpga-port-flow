# V80 Deploy Manager QDMA Dry-Run Verification

## Date: 2026-08-05

## Test file
`$FIRESIM/deploy/tests/test_v80_deploy_manager.py`

## What was tested
Four verification categories with 78 total checks:

### (A) Import & instantiation (29 tests)
- Class imports without errors
- All 9 expected methods exist with correct type signatures
- All V80-specific methods are defined on the V80 class (not just inherited)
- PLATFORM_NAME is set to 'xilinx_alveo_v80'

### (B) QDMA BDF encoding (13 tests)
- `_compute_qdma_bdf('b1:00.0')` = 724992 = 0xb1000
- `_compute_qdma_bdf('3b:00.0')` = 241664 = 0x3b000
- `_compute_qdma_bdf('86:00.1')` = 548865 = 0x86001
- Edge cases: 00:00.0 = 0, ff:1f.7 = 0xff1f7
- 5-digit hex formatting verified for all

### (C) Command sequence audit (13 tests)
- load_qdma: qmax set BEFORE q add BEFORE q start ✓
- load_qdma: uses 'mode mm dir bi' (not streaming) ✓
- flash_fpgas: PCIe rescan AFTER vivado programming ✓
- flash_fpgas: disconnect BEFORE programming ✓
- unload_qdma: q stop BEFORE q del BEFORE modprobe -r ✓
- modprobe uses 'qdma-pf' (hyphen) for module alias ✓
- lsmod uses 'qdma_pf' (underscore) for kernel name ✓

### (D) C++ driver cross-check (23 tests)
- BDF encoding formula matches: (bus<<12)|(dev<<4)|func in both C++ and Python
- BAR index = 1 in both C++ driver and Python start_sim_slot
- BAR size = 32 MB (0x2000000 = 2^25, matches CtrlNastiKey addrBits=25)
- Device file pattern: C++ /dev/qdma%05x-MM-0 matches Python queue setup (mode mm, idx 0)
- PCI IDs match: vendor=0x10ee, device=0x903f in both

## Bugs during test development
1. **Regex for C++ BDF pattern**: Initial regex `\(.*bus.*<<\s*12\)` didn't match because
   C++ uses `((uint32_t)bus_id << 12)` — needed to search for `bus_id\s*<<\s*12` with DOTALL.
2. **Rescan position check**: `flash_fpgas_src.find("rescan")` found the docstring mention
   (char 295) before the actual `/sys/bus/pci/rescan` command (char 3842). Fixed by searching
   for the full sysfs path instead.
