---
id: CHIPYARD-STEP6-PART1-ITER1
repo: CHIPYARD
step: 6
part: 1
iter: 1
parent: FIRESIM-STEP6-PART1-ITER1
timestamp: 2026-08-05T06:23:08.901886+00:00
git_hash: STDERR:
---

# step6/part1: Built the bare workload RISC-V binary (hello.c + crt.S + syscalls.c → hello ELF) by cross-compiling with riscv64-unknown-elf-gcc. The original source directory at /home/ray/chipyard/software/firemarsh

## Message

Built the bare workload RISC-V binary (hello.c + crt.S + syscalls.c → hello ELF) by cross-compiling with riscv64-unknown-elf-gcc. The original source directory at /home/ray/chipyard/software/firemarshal/test/bare/ is read-only (owned by uid 1000, container runs as uid 19696), so the build was done in /tmp/bare/ and the binary was also copied to $FIRESIM/deploy/workloads/bare/hello (persistent NFS-mounted location). The binary is verified as 'ELF 64-bit LSB executable, UCB RISC-V, version 1 (SYSV), statically linked, not stripped' with entry point 0x80000000.

## Diff

```diff

STDERR:
error: Could not access 'STDERR:'

[exit code: 1]
```

## Files modified

- (none)
