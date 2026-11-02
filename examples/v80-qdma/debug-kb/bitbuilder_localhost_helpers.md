# BitBuilder Localhost SSH Bypass

## Problem
FireSim's BitBuilder uses Fabric's `run()` and `rsync_project()` which require SSH
even to localhost, but no sshd is accessible from the V80 container.

## Solution
Added three helper methods to BitBuilder base class:
1. `_is_localhost()` — checks if `env.host_string` is 'localhost' or '127.0.0.1'
2. `_exec(cmd, **kwargs)` — dispatches to `local(cmd, capture=True)` for localhost, `run()` for remote
3. `_rsync_files(local_dir, remote_dir, upload, exclude, extra_opts)` — dispatches to `local('rsync -aL ...')` for localhost, `rsync_project()` for remote

Modified methods:
- `BitBuilder.replace_rtl()` — `run()` → `self._exec()`
- `BitBuilder.build_driver()` — `run()` → `self._exec()`
- `XilinxAlveoBitBuilder.cl_dir_setup()` — `run()` → `self._exec()`, `rsync_project()` → `self._rsync_files()`
- `XilinxAlveoBitBuilder.build_bitstream()` — `run()` → `self._exec()`, `rsync_project()` → `self._rsync_files()`

## Key findings
- Python ABCMeta blocks `__new__()` on abstract classes in Python 3.12+ — need concrete subclass for testing
- Fabric 1.x `prefix()` context manager DOES work with `local()` — verified: `export` and `cd` prefixes propagate correctly
- For local rsync, omit `-e ssh` entirely — just use `rsync -aL [extra_opts] [exclude_args] <src> <dst>`
- Unmodified classes (F2BitBuilder, VitisBitBuilder, XilinxVCU118BitBuilder, etc.) continue using `run()`/`rsync_project()` directly

## Date
2026-08-05
