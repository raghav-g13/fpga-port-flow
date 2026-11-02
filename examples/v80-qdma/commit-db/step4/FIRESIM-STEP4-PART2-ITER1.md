---
id: FIRESIM-STEP4-PART2-ITER1
repo: FIRESIM
step: 4
part: 2
iter: 1
parent: CHIPYARD-STEP4-PART1-ITER1
timestamp: 2026-08-05T04:20:01.941231+00:00
git_hash: STDERR:
---

# step4/part2: Re-elaborated F1Shim for V80 config with 32 GiB HostMemChannelKey. Overcame multiple build obstacles: (1) fixed coursier cache permissions by redirecting to /tmp, (2) fixed broken FIRRTL/anno symlinks

## Message

Re-elaborated F1Shim for V80 config with 32 GiB HostMemChannelKey. Overcame multiple build obstacles: (1) fixed coursier cache permissions by redirecting to /tmp, (2) fixed broken FIRRTL/anno symlinks by copying pre-partition artifacts, (3) stripped conflicting annotations from the anno file (TargetDirAnnotation, ConfigPackageAnnotation, FirrtlCircuitAnnotation), (4) symlinked firechip goldengateimplementations+bridgeinterfaces into midas target-symlinks to include BlockDevBridgeModule etc. in the JAR, (5) rebuilt firesim-main.jar and ran GoldenGate directly. The regenerated FireSim-generated.sv now shows 35-bit slave addresses (was 33-bit with old 8 GiB config). Recorded all 6 requested port widths: io_slave_0_aw_bits_addr=[34:0]=35, io_slave_0_ar_bits_addr=[34:0]=35, io_pcis_aw_bits_id=[15:0]=16, io_master_aw_bits_addr=[24:0]=25, io_slave_0_w_bits_data=[63:0]=64, io_slave_0_aw_bits_id=[15:0]=16. Saved reference to $REFERENCES/firesim/v80_f1shim_port_widths.md.

## Diff

```diff

STDERR:
error: Could not access 'STDERR:'

[exit code: 1]
```

## Files modified

- (none)
