# Bug 001: Fabric local() uses /bin/sh (dash) which doesn't support `source`

## Symptom
`firesim buildbitstream` fails immediately with:
```
/bin/sh: 1: source: not found
```

## Root Cause
- Fabric's `local()` function uses `subprocess.Popen(cmd, shell=True)` which defaults to `/bin/sh`
- On Ubuntu, `/bin/sh` is `dash`, which is POSIX sh and does not support the `source` builtin (uses `.` instead)
- The `replace_rtl()` method uses `prefix("source sourceme-manager.sh --skip-ssh-setup")` which wraps the make command with `source ...`
- Additionally, `sourceme-manager.sh` internally calls `source ./env.sh`, so changing `source` to `.` in just the prefix wouldn't be sufficient

## Fix
Modified `_exec()` in `bitbuilder.py` to pass `shell="/bin/bash"` to `local()`:
```python
return local(cmd, capture=True, shell="/bin/bash")
```
This makes Fabric use bash as the shell executable for local commands, which supports `source`.
Also applied the same fix to `_rsync_files()` for consistency.

## Files Modified
- `$FIRESIM/deploy/buildtools/bitbuilder.py` (lines 77, 93)

# Bug 002: Java 20 Security Manager deprecation breaks SBT

## Symptom
SBT fails during initialization with:
```
java.io.IOException: Permission denied
    at java.base/java.io.UnixFileSystem.createFileExclusively0(Native Method)
    at java.base/java.io.File.createTempFile(File.java:2181)
    at sbt.StandardMain$.$anonfun$initialGlobalLogging$1(Main.scala:242)
```

## Root Cause
- The container uses Java 20 (OpenJDK 20.0.2-internal)
- Java 18+ deprecated `java.lang.SecurityManager` and Java 20 throws when SBT tries to use it
- SBT 1.1.1 calls `System.setSecurityManager()` during initialization
- The misleading "Permission denied" message is actually from the Security Manager removal

## Fix
Added `-Djava.security.manager=allow` to `JAVA_TOOL_OPTIONS` in `$FIRESIM/sim/make/scala-build.mk`:
```
export JAVA_TOOL_OPTIONS ?= -Xmx$(JAVA_HEAP_SIZE) -Xss8M -Djava.io.tmpdir=$(firesim_base_dir)/.java_tmp -Djava.security.manager=allow
```

## Additional Fix: CLASSPATH_CACHE permission
- `$CHIPYARD/.classpath_cache/` is owned by `ray:users` and not writable by uid 19696
- Created writable `$FIRESIM/sim/.classpath_cache/` and modified `make_recipe()` to override `CLASSPATH_CACHE`

## Files Modified
- `$FIRESIM/sim/make/scala-build.mk` (line 36)
- `$FIRESIM/deploy/buildtools/buildconfig.py` (line 264)

# Bug 003: Wrong default_build_dir causes nested directory paths

## Symptom
During `build_bitstream`, `cl_dir_setup` creates the build directory at a wrong nested path:
`$FIRESIM/platforms/xilinx_alveo_v80/cl_firesim/platforms/xilinx_alveo_v80/cl_<quintuplet>`
instead of:
`$FIRESIM/platforms/xilinx_alveo_v80/cl_<quintuplet>`

## Root Cause
`default_build_dir` in `config_build.yaml` was set to `.../cl_firesim` (the template dir).
`cl_dir_setup` constructs `dest_alveo_dir = dest_build_dir + "/platforms/" + PLATFORM`.
This results in `.../cl_firesim/platforms/xilinx_alveo_v80/`.

## Fix
Changed `default_build_dir` to `$FIRESIM` root (`/home/ray/chipyard/sims/firesim`).
Now: `dest_alveo_dir = $FIRESIM/platforms/xilinx_alveo_v80` (correct).

## Files Modified
- `$FIRESIM/deploy/config_build.yaml`
- `$FIRESIM/deploy/build-farm-recipes/externally_provisioned.yaml`
