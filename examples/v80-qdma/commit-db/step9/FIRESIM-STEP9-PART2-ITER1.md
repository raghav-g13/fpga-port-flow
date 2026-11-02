---
id: FIRESIM-STEP9-PART2-ITER1
repo: FIRESIM
step: 9
part: 2
iter: 1
parent: CHIPYARD-STEP9-PART1-ITER1
timestamp: 2026-08-05T17:36:23.686591+00:00
git_hash: 5efbc4ef60acec8150813f67e80c00140c9199d6
---

# step9/part2: Added three localhost-aware helper methods to BitBuilder base class: (1) _is_localhost() checks if env.host_string is 'localhost' or '127.0.0.1' (strips user@/port); (2) _exec(cmd, **kwargs) dispatche

## Message

Added three localhost-aware helper methods to BitBuilder base class: (1) _is_localhost() checks if env.host_string is 'localhost' or '127.0.0.1' (strips user@/port); (2) _exec(cmd, **kwargs) dispatches to local(cmd, capture=True) for localhost or run() for remote; (3) _rsync_files(local_dir, remote_dir, upload, exclude, extra_opts) dispatches to local('rsync -aL ...') without -e ssh for localhost or rsync_project() for remote. Modified BitBuilder.replace_rtl() and build_driver() to use self._exec() instead of run(). Modified XilinxAlveoBitBuilder.cl_dir_setup() to use self._exec() and self._rsync_files(). Modified XilinxAlveoBitBuilder.build_bitstream() to use self._exec() (with settings(warn_only=True) preserved) and self._rsync_files(). All other builders (F2, Vitis, VCU118, RHSResearch, etc.) are untouched.

## Diff

```diff

```

## Files modified

- `$FIRESIM/deploy/buildtools/bitbuilder.py`
