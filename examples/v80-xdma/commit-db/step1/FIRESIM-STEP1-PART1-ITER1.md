---
id: FIRESIM-STEP1-PART1-ITER1
repo: FIRESIM
step: 1
part: 1
iter: 1
parent: BASE
timestamp: 2026-01-15T10:30:00Z
---

# Add Xilinx Alveo V80 platform directory with XDMA shell

## Message

Create the initial V80 platform directory structure under `$FIRESIM/platforms/xilinx_alveo_v80/`.
Adds the XDMA-based shell wrapper, board constraints (XDC), and Vivado IP TCL scripts
adapted from the U250 XDMA platform.

## Diff

```diff
diff --git a/platforms/xilinx_alveo_v80/cl_firesim/scripts/create_bd.tcl b/platforms/xilinx_alveo_v80/cl_firesim/scripts/create_bd.tcl
new file mode 100644
--- /dev/null
+++ b/platforms/xilinx_alveo_v80/cl_firesim/scripts/create_bd.tcl
@@ -0,0 +1,12 @@
+# V80 block design: XDMA bridge + AXI interconnect
+create_bd_design "design_1"
+
+# XDMA IP configured for x16 Gen4
+create_bd_cell -type ip -vlnv xilinx.com:ip:xdma:4.1 xdma_0
+set_property -dict [list \
+    CONFIG.pcie_blk_locn {PCIE4CE_X1Y0} \
+    CONFIG.pl_link_cap_max_link_width {X16} \
+    CONFIG.pl_link_cap_max_link_speed {8.0_GT/s} \
+    CONFIG.axi_data_width {512_bit} \
+    CONFIG.axisten_freq {250} \
+] [get_bd_cells xdma_0]
```

## Files modified

- `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/scripts/create_bd.tcl`: XDMA block design TCL
