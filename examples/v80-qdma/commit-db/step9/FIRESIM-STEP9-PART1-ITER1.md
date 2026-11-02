---
id: FIRESIM-STEP9-PART1-ITER1
repo: FIRESIM
step: 9
part: 1
iter: 1
parent: BASE
timestamp: 2026-08-05T17:25:08.315949+00:00
git_hash: 5efbc4ef60acec8150813f67e80c00140c9199d6
---

# step9/part1: Created LD_PRELOAD shared library (nss_uid_fix.so) that intercepts getpwuid/getpwnam/getpwuid_r/getpwnam_r to map container UID 19696 → user 'ray' with home=/home/ray. Also created firesim-local wrapp

## Message

Created LD_PRELOAD shared library (nss_uid_fix.so) that intercepts getpwuid/getpwnam/getpwuid_r/getpwnam_r to map container UID 19696 → user 'ray' with home=/home/ray. Also created firesim-local wrapper script that sets LD_PRELOAD before invoking the real firesim Python entry-point. Verified all four NSS functions work correctly, other users (root) still resolve via fallthrough to glibc, and firesim-local --help runs successfully.

## Diff

```diff

```

## Files modified

- `$FIRESIM/deploy/nss_uid_fix.c`
- `$FIRESIM/deploy/nss_uid_fix.so`
- `$FIRESIM/deploy/firesim-local`
