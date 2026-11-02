---
id: CHIPYARD-STEP4-PART1-ITER1
repo: CHIPYARD
step: 4
part: 1
iter: 1
parent: FIRESIM-STEP4-PART1-ITER1
timestamp: 2026-08-05T03:49:58.667980+00:00
git_hash: STDERR:
---

# step4/part1: Made three changes to Config.scala: (a) Changed XilinxAlveoV80Config's HostMemChannelKey size from 0x200000000L (8 GiB) to 0x800000000L (32 GiB) to match V80's actual DDR4 capacity. (b) Reverted F1Con

## Message

Made three changes to Config.scala: (a) Changed XilinxAlveoV80Config's HostMemChannelKey size from 0x200000000L (8 GiB) to 0x800000000L (32 GiB) to match V80's actual DDR4 capacity. (b) Reverted F1Config's CPUManagedAXI4Key idBits from 16 back to 6 (removed the stale commented-out line and restored original value, since the 16-bit change was V80-specific and could break F1). (c) Added an explicit CPUManagedAXI4Key override in XilinxAlveoV80Config with addrBits=64, dataBits=512, idBits=16.

## Diff

```diff

STDERR:
error: Could not access 'STDERR:'

[exit code: 1]
```

## Files modified

- `$FIRESIM/sim/midas/src/main/scala/midas/Config.scala`
