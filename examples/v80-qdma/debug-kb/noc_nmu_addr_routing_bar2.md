# Bug: NoC NMU $fatal on BAR2 MMIO access — Address Routing Fix

**Date**: 2026-08-04
**Step**: F1Shim MMIO simulation test (bar_test0)
**Severity**: Critical (simulation-blocking)

## Symptom

VCS simulation of `bar_test0` hit `$fatal` from `nmu_addr_map.sv:87`:
```
REG_SRC =256 dest_id should be generated from REMAPPED registers 
for addr('h20180000224) in PL_VIA_NOC address space
```

## Root Cause Chain

**Issue 1: NMU missing address decode entry for BAR2**
- The CPM5 BFM translates PCIe BAR2 address `0x80224` to NoC address `0x020180000224`
- The NMU (`axi_noc_0/S00_AXI_nmu`, REG_SRC=0x100) only had entries for:
  - MADDR0=0x02010000 (PCIE_M_AXI_LITE at 0x020100000000, 32MB)
  - MADDR1=0x02030000 (DDR4 at 0x020300000000, 4GB)
- Address 0x02018000 (addr[47:16] of 0x020180000224) didn't match → NMU $fatal

**Issue 2: After MADDR fix, SmartConnect returned DECERR (0xdec0dee3)**
- With identity RPADDR (0x02018000), the remapped address stayed 0x020180000224
- The SmartConnect between NoC NSU and PCIE_M_AXI_LITE was configured for segment at 0x020100000000 (32M range)
- 0x020180000224 is 0x80000000 (2GB) above the base — outside 32M range → DECERR

## Fix (nocattrs.dat)

Added NMU address decode region 2 for BAR2 traffic with address remapping:

```
REG_ADDR_MADDR2  = 02018000  (match CPM5's BAR2 output in addr[47:16])
REG_ADDR_MASK2   = fffffff0  (1MB coverage, > 128KB BAR)
REG_ADDR_RPADDR2 = 02010000  (REMAP to expected segment base!)
REG_ADDR_DST2    = 00000040  (route to M01_AXI_nsu = PCIE_M_AXI_LITE)
REG_ADDR_ENABLE  = 00000007  (enable regions 0,1,2)
REG_ADDR_REMAP   = 00000007  (remap on regions 0,1,2)
```

The key insight: RPADDR2 must be 0x02010000 (NOT identity 0x02018000).
The NMU remap formula `(input & ~MASK) | (RPADDR & MASK)` maps
0x02018000 → 0x02010000, placing the address inside the SmartConnect's 32M segment.

## Address Flow (after fix)

```
PCIe BAR2+0x224 → CPM5 → NoC addr 0x020180000224
→ NMU MADDR2 match (0x02018000 & 0xFFFFFFF0)
→ Remap to 0x020100000224 (RPADDR2=0x02010000)
→ Route to M01_AXI_nsu (DST2=0x40)
→ SmartConnect matches segment at 0x020100000000 (32M)
→ Output addr 0x224 on PCIE_M_AXI_LITE
→ F1Shim receives bits[24:0] = 0x224
→ PRESENCE_READ returns 0x46697265 ✓
```

## Files Modified

- `$CL_DIR/vcs/vcs/nocattrs.dat` — 6 lines changed (MADDR2, MASK2, RPADDR2, DST2, ENABLE, REMAP)

## Verification

bar_test0 results after fix:
- CDO programming done ✅
- PCIe link-up (user_lnk_up=1, LTSSM=0x10) ✅  
- SYSTEM CHECK PASSED ✅
- PRESENCE_READ = 0x46697265 ("Fire") ✅
- INIT_DONE = 1 ✅
- Write 0xDEADBEEF → readback 0xDEADBEEF ✅
- PeekPoke DONE = 1 ✅
- bar_test0 PASSED ✅
- $finish reached, no $fatal ✅
