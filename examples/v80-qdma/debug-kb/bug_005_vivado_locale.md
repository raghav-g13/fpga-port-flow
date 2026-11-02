# Bug 005: Vivado locale crash in container

## Symptom
Vivado exits with SIGABRT (return code 134):
```
terminate called after throwing an instance of 'std::runtime_error'
  what():  locale::facet::_S_create_c_locale name not valid
```

## Root Cause
`/ecad/tools/xilinx/2025.1/Vivado/bin/rdiArgs.sh` line 37 sets `LC_ALL=en_US.UTF-8`, but the Docker container only has `C`, `C.utf8`, and `POSIX` locales.

## Fix
In `build-bitstream.sh`, before the vivado call, copy C.utf8 locale data to create en_US.UTF-8:
```bash
if [ ! -d /usr/lib/locale/en_US.UTF-8 ] && [ -d /usr/lib/locale/C.utf8 ]; then
    mkdir -p /tmp/locales/en_US.UTF-8
    cp -r /usr/lib/locale/C.utf8/* /tmp/locales/en_US.UTF-8/ 2>/dev/null
    export LOCPATH=/tmp/locales
fi
```

## Files Modified
- `$FIRESIM/platforms/xilinx_alveo_v80/build-bitstream.sh`
