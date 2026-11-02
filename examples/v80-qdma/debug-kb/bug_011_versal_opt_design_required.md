# Bug 011: Versal requires opt_design before place_design

## Symptom
`place_design -directive Quick` fails immediately with:
```
ERROR: [Vivado_Tcl 4-414] Found memory core or Advanced IO Wizard core that needs to be (re)generated. Please run opt_design or implement_xphy_cores prior to launching place_design.
```

## Environment
- Vivado 2025.1
- Part: xcv80-lsva4737-2MHP-e-S (Versal ACAP V80)
- Flow_Quick strategy with `opt 0` (opt_design disabled)

## Root Cause
On Versal devices, `opt_design` (or `implement_xphy_cores`) is REQUIRED before `place_design`. The Versal architecture has XPHY cores for DDR4 I/O and memory controllers that must be processed by opt_design. This is different from UltraScale+ (U250/U280) where opt_design can be skipped.

## Fix
Changed Flow_Quick strategy to enable opt_design:
```tcl
set opt 1
set opt_directive "Default"
```

## Additional Fix: Empty property values
The `set_property -dict` call in implementation.tcl also failed with `[Common 17-110] Invalid property value` when any directive or option was an empty string. Fixed by using individual `set_property` calls with empty-value checks:
```tcl
proc set_prop_if_nonempty { prop val obj } {
    if {$val ne ""} {
        set_property $prop $val $obj
    }
}
```

## Files Modified
- `scripts/strategies/strategy_Flow_Quick.tcl` — enabled opt_design
- `scripts/implementation.tcl` — individual set_property with empty-value protection
