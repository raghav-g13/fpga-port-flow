# VCS Simulation Setup Debug Log

## Bug 1: VCS shebang incompatibility with dash
- **Error**: `/bin/sh: 0: Illegal option -h`
- **Root cause**: VCS scripts (vlogan, vhdlan, vcs) use `#!/bin/sh -h` shebang. On Ubuntu 22.04, `/bin/sh -> dash`, and dash doesn't support the `-h` flag (which means "hash all" in ksh/bash).
- **Fix**: Create a patched VCS installation at `/tmp/vcs_patched/` that symlinks everything except `bin/`, copies `bin/` and fixes all shebangs from `#!/bin/sh -h` to `#!/bin/bash -h`.
- **Affected files**: 49 scripts in VCS bin/ directory

## Bug 2: /usr/bin/time missing in container
- **Error**: `/tmp/vcs_patched/bin/vcs: line 14339: /usr/bin/time: No such file or directory`
- **Root cause**: VCS script hardcodes `/usr/bin/time` for timing. GNU time is not installed in the container.
- **Fix**: Created a wrapper at `/tmp/bin_fixes/time` that strips timing flags (-p, -f, -o, --append) and exec's the remaining command. Replaced all `/usr/bin/time` references in the patched vcs script with `/tmp/bin_fixes/time`.
- **Initial wrong fix**: Replacing `/usr/bin/time -f` with `# time -f` caused `eval` statements to treat everything after `#` as a comment, silently skipping the actual VCS elaboration command.

## Bug 3: VCS_ARCH_OVERRIDE=linux vs linux64
- **Error**: `Sorry, Linux version 6.8.0-124-generic is not supported`
- **Root cause**: `VCS_ARCH_OVERRIDE=linux64` is NOT a valid value. The vlsi.bashrc sets `VCS_ARCH_OVERRIDE=linux` which bypasses kernel version checking. The `-full64` flag in vlogan_opts/vcs_elab_opts forces 64-bit binary usage.
- **Fix**: Keep `VCS_ARCH_OVERRIDE=linux` (don't change to linux64).

## Bug 4: libelf.so.1 missing for 64-bit VCS
- **Error**: `libelf.so.1: cannot open shared object file`
- **Root cause**: 64-bit vcs1 binary needs libelf.so.1 which isn't in the default LD_LIBRARY_PATH.
- **Fix**: Add `/home/ray/chipyard/.conda-env/lib` to LD_LIBRARY_PATH (conda provides libelf.so.1).

## Bug 5: XMRE cross-module reference errors (247 errors)
- **Error**: `Error-[XMRE] Cross-module reference resolution error` for `board.EP.design_1_wrapper_i.design_1_i.axi_bram_ctrl_0.*`
- **Root cause**: The `COMPARE_DATA_H2C` task in `usp_pci_exp_usrapp_tx.v` (Xilinx QDMA BFM code) contains cross-module references to `axi_bram_ctrl_0` which exists in the CED design but NOT in the FireSim design hierarchy.
- **Fix**: Wrapped the `COMPARE_DATA_H2C` task body with `` `ifdef FIRESIM_EP `` guard. When FIRESIM_EP is defined (which it is via `+define+FIRESIM_EP=` in vlogan commands), a stub task is used instead.
- **Note**: `-suppress=XMRE` and `-error=noXMRE` VCS flags did NOT work to suppress these errors.

## Bug 6: libncurses.so.5 missing for VCS internal clang
- **Error**: `libncurses.so.5: cannot open shared object file`
- **Root cause**: VCS's internal clang (3.4.2) needs libncurses.so.5, but Ubuntu 22.04 only has .so.6.
- **Fix**: Create symlink `/tmp/libncurses.so.5 -> /usr/lib/x86_64-linux-gnu/libncurses.so.6` and add `/tmp` to LD_LIBRARY_PATH.
