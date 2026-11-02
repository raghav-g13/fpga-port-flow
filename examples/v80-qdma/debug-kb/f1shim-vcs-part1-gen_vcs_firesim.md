# F1Shim VCS Part 1: gen_vcs_firesim.tcl + synopsys_sim.setup

## Date: 2026-08-03

## Task
Create gen_vcs_firesim.tcl to export VCS simulation scripts from the existing firesim.xpr Vivado project.

## Bugs Encountered

### Bug 1: Vivado locale crash (en_US.UTF-8 not available)
- **Symptom**: `terminate called after throwing an instance of 'std::runtime_error' what(): locale::facet::_S_create_c_locale name not valid`
- **Root Cause**: Vivado's `/ecad/tools/xilinx/2025.1/Vivado/bin/rdiArgs.sh` (line 37) hardcodes `export LC_ALL="en_US.UTF-8"`, but the container only has `C` and `C.utf8` locales. The `/ecad` mount is read-only.
- **Fix**: Create a fake `en_US.UTF-8` locale from `C.utf8`: `cp -a /usr/lib/locale/C.utf8 /tmp/locale/en_US.UTF-8` then set `LOCPATH=/tmp/locale:/usr/lib/locale` before running Vivado.

### Bug 2: Vivado libtinfo.so.5 missing
- **Symptom**: `couldn't load file "libxv_commontasks.so": libtinfo.so.5: cannot open shared object file`
- **Root Cause**: Container has libtinfo.so.6 but Vivado needs libtinfo.so.5.
- **Fix**: `ln -sf /usr/lib/x86_64-linux-gnu/libtinfo.so.6 /tmp/libtinfo.so.5` then add `/tmp` to `LD_LIBRARY_PATH`.

### Bug 3: Tcl `**` glob not recursive
- **Symptom**: PIPESIM patches not applied; glob returned 0 files.
- **Root Cause**: Tcl's `glob` command does NOT support `**` for recursive directory matching (unlike bash). The pattern `"$proj_dir/firesim.gen/sources_1/bd/design_1/**/bd_*_cpm_0_0.sv"` matched nothing.
- **Fix**: Implemented a recursive `find_files` Tcl proc that walks directories manually.

### Bug 4: Auto-detect path wrong (3 levels vs 2)
- **Symptom**: Auto-detection couldn't find cl_xilinx_alveo_v80-* directory.
- **Root Cause**: Script at `cl_firesim/verif/` needs to go 2 levels up (`../../`) to reach `xilinx_alveo_v80/`, not 3 levels (`../../../`). The original setup_xsim.tcl had the same bug but was never tested without explicit CL_DIR argument.
- **Fix**: Changed `/../../../cl_xilinx_alveo_v80-*` to `/../../cl_xilinx_alveo_v80-*`.

## Environment Setup for Vivado in Container
```bash
export LOCPATH=/tmp/locale:/usr/lib/locale
export LD_LIBRARY_PATH=/tmp:$LD_LIBRARY_PATH
# Requires one-time setup:
#   mkdir -p /tmp/locale && cp -a /usr/lib/locale/C.utf8 /tmp/locale/en_US.UTF-8
#   ln -sf /usr/lib/x86_64-linux-gnu/libtinfo.so.6 /tmp/libtinfo.so.5
```

## Files Modified
1. `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/verif/gen_vcs_firesim.tcl` (new)
2. `$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/verif/vcs_xilinx_lib/synopsys_sim.setup` (path fix)
