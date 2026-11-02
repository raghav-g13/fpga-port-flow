# Bare Workload Build - Permission Issue

## Date: 2026-08-04

## Issue
Cannot write build artifacts to `/home/ray/chipyard/software/firemarshal/test/bare/` because:
- Directory is owned by `ray` (uid 1000) with permissions `755`
- Container runs as uid 19696 (non-root, no special capabilities)
- No sudo, no setfacl, no unshare, no runuser available

## Root Cause
The chipyard source tree is part of the Docker image layer (overlay filesystem). While the overlay is technically rw, Unix file permissions prevent uid 19696 from writing to directories owned by uid 1000 with 755 permissions.

## Workaround
1. Copied source files to `/tmp/bare/` (writable)
2. Built there successfully with `make`
3. Also copied binary to `/home/ray/chipyard/sims/firesim/deploy/workloads/bare/hello` (NFS-mounted, writable)

## Binary Locations
- `/tmp/bare/hello` - temp location (lost on container restart)
- `$FIRESIM/deploy/workloads/bare/hello` - persistent location (NFS-mounted)

## Binary Verification
- Type: ELF 64-bit LSB executable, UCB RISC-V, version 1 (SYSV), statically linked, not stripped
- Size: 13968 bytes
- Entry point: 0x80000000
- Machine: RISC-V, Class: ELF64

## Build Command
```
bash -c 'source /home/ray/chipyard/sims/firesim/env.sh && make -C /tmp/bare/'
```

## Build Output
Compiled successfully: hello.c → hello.o, crt.S → crt.o, syscalls.c → syscalls.o → linked to `hello`
Only warnings (format specifier, unused variables), no errors.
