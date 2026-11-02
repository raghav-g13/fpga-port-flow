# NSS UID Fix Implementation

**Date**: 2026-08-05
**Component**: Container UID mismatch workaround
**Status**: Resolved

## Problem

The V80 chipyard container runs processes as UID 19696 (the host user), but
`/etc/passwd` inside the container only has `ray:x:1000`. This causes:

- `pwd.getpwuid(19696)` → `KeyError: 'getpwuid(): uid not found: 19696'`
- `getpass.getuser()` → same crash (calls getpwuid internally)
- Fabric/Paramiko SSH client → fails during SSH setup
- `os.path.expanduser("~")` → may fail or return wrong path

## Solution

Created an `LD_PRELOAD` shared library (`nss_uid_fix.so`) that intercepts four
POSIX NSS entry points:

- `getpwuid()` / `getpwnam()` — return static `struct passwd`
- `getpwuid_r()` / `getpwnam_r()` — fill caller-supplied buffer (thread-safe)

When the queried UID is 19696 or name is "ray", the shim returns a synthetic
passwd entry: `{ ray, x, 19696, <real_gid>, "", /home/ray, /bin/bash }`.
All other lookups fall through to glibc via `dlsym(RTLD_NEXT, ...)`.

## Files Created

- `$FIRESIM/deploy/nss_uid_fix.c` — C source
- `$FIRESIM/deploy/nss_uid_fix.so` — compiled shared library
- `$FIRESIM/deploy/firesim-local` — wrapper script that sets LD_PRELOAD

## Verification

```
LD_PRELOAD=$FIRESIM/deploy/nss_uid_fix.so python3 -c 'import getpass; print(getpass.getuser())'
# → ray

# Also verified: pwd.getpwuid, pwd.getpwnam, root fallthrough, expanduser, firesim-local --help
```
