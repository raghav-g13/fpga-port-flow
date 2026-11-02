# Bug 006: Vivado libtinfo.so.5 missing

## Symptom
Vivado silently fails with exit code 0:
```
application-specific initialization failed: couldn't load file "libxv_commontasks.so": libtinfo.so.5: cannot open shared object file
```

## Root Cause
Container has libtinfo.so.6 but Vivado requires libtinfo.so.5. Compatibility symlinks exist at `/tmp/libtinfo.so.5` and `/tmp/libncurses.so.5` but /tmp is not on LD_LIBRARY_PATH.

## Fix
In `build-bitstream.sh`:
```bash
if [ -f /tmp/libtinfo.so.5 ]; then
    export LD_LIBRARY_PATH=/tmp:${LD_LIBRARY_PATH}
fi
```

## Files Modified
- `$FIRESIM/platforms/xilinx_alveo_v80/build-bitstream.sh`
