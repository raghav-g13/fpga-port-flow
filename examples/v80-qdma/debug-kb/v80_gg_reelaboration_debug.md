# V80 GoldenGate Re-elaboration Debug Log

## Date: 2026-08-04

## Issue
Need to re-elaborate F1Shim RTL after changing V80 HostMemChannelKey.size from 8 GiB (0x200000000L) to 32 GiB (0x800000000L).

## Obstacles Encountered

### 1. SBT coursier cache permission denied
- **Root cause**: Container UID 19696 cannot write to `/home/ray/.cache/coursier/v1/.structure.lock` (owned by UID 1000/ray)
- **Fix**: Set `COURSIER_CACHE=/tmp/coursier-cache` and copy existing cache there

### 2. Chipyard SBT java.io.tmpdir not writable
- **Root cause**: `/home/ray/chipyard/.java_tmp` owned by ray, not writable by container UID
- **Fix**: Set `JAVA_TOOL_OPTIONS="-Xmx16G -Xss8M -Djava.io.tmpdir=/tmp/chipyard_java_tmp"`

### 3. Chipyard .classpath_cache not writable
- **Root cause**: `/home/ray/chipyard/.classpath_cache/` owned by ray
- **Workaround**: Skip chipyard-level SBT entirely; rebuild firesim-main.jar only

### 4. FIRRTL symlinks broken
- **Root cause**: Symlinks point to `/home/ray/chipyard/` which is not mounted in container
- **Fix**: Replace broken symlinks with copies of `pre-partition.fir` and `pre-partition-all.json`

### 5. Duplicate annotations in anno file
- **Root cause**: `pre-partition-all.json` contains `TargetDirAnnotation` and `ConfigPackageAnnotation` from previous run
- **Fix**: Python script to strip `firrtl.options.TargetDirAnnotation`, `firrtl.transforms.BlackBoxTargetDirAnno`, `midas.stage.ConfigPackageAnnotation`, `midas.stage.ConfigStringAnnotation`, `midas.stage.OutputBaseFilenameAnnotation`, `firrtl.stage.FirrtlFileAnnotation`, `firrtl.options.InputAnnotationFileAnnotation`, `firrtl.stage.AllowUnrecognizedAnnotation`, `firrtl.annotations.DeletedAnnotation`, `firrtl.stage.FirrtlCircuitAnnotation`, `midas.stage.phases.ConfigParametersAnnotation`

### 6. Missing firechip classes in JAR
- **Root cause**: Default `make firesim-main-classpath` doesn't include firechip `goldengateimplementations` and `bridgeinterfaces`
- **Fix**: Symlink firechip source dirs into `midas/src/main/scala/target-symlinks/` before building JAR

## Successful Command

```bash
export COURSIER_CACHE=/tmp/coursier-cache
export JAVA_TOOL_OPTIONS="-Xmx16G -Xss8M -Djava.io.tmpdir=/tmp/chipyard_java_tmp"

# Symlink firechip sources
SYMLINK_DIR=$CHIPYARD/sims/firesim/sim/midas/src/main/scala/target-symlinks
mkdir -p $SYMLINK_DIR/{goldengateimplementations,bridgeinterfaces}
ln -sf $CHIPYARD/generators/firechip/goldengateimplementations/src $SYMLINK_DIR/goldengateimplementations/src
ln -sf $CHIPYARD/generators/firechip/bridgeinterfaces/src $SYMLINK_DIR/bridgeinterfaces/src

# Rebuild JAR with firechip classes
make firesim-main-classpath

# Run GoldenGate directly
java -cp $JAR midas.stage.GoldenGateMain \
  -i ${GENDIR}/firechip.chip.FireSim.FireSimRocket8GiBDRAMConfig.fir \
  -td ${GENDIR} \
  -faf ${GENDIR}/firechip.chip.FireSim.FireSimRocket8GiBDRAMConfig.anno.json \
  -ggcp firesim.configs \
  -ggcs BaseXilinxAlveoV80Config \
  --output-filename-base FireSim-generated \
  --allow-unrecognized-annotations \
  --no-dedup
```

## Result
Successfully regenerated FireSim-generated.sv with 35-bit slave addresses (was 33-bit).
