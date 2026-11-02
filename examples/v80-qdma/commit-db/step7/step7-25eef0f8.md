---
step: 7
id: step7-25eef0f8
status: active
created: 2026-08-05T07:23:29.914125+00:00
---

# Step 7 checkpoint

## Commit sequence

1. `FIRESIM-STEP7-PART1-ITER1`
2. `CHIPYARD-STEP7-PART1-ITER1`
3. `FIRESIM-STEP7-PART2-ITER1`
4. `CHIPYARD-STEP7-PART2-ITER1`
5. `FIRESIM-STEP7-PART3-ITER1`
6. `CHIPYARD-STEP7-PART3-ITER1`

## Verification

Part 1: ['Verified elif condition in deploy/firesim line 187 includes \'or args.platform == "xilinx_alveo_v80"\'', "Verified deploy_manager_map contains 'xilinx_alveo_v80': 'XilinxAlveoV80InstanceDeployManager'", 'Verified XilinxAlveoV80InstanceDeployManager class exists at line 1447 of run_farm_deploy_managers.py', "Ran 'firesim managerinit --platform xilinx_alveo_v80' — output shows 'Adding default overrides to config files' with NO 'Unknown platform' message", "Confirmed config_runtime.yaml contains 'default_platform: XilinxAlveoV80InstanceDeployManager'", "Confirmed zero occurrences of 'Unknown platform' in the managerinit log", 'Validated config_runtime.yaml parses as valid YAML without errors']
Part 2: ['Tarball exists at deploy/built-hwdb-entries/xilinx_alveo_v80_firesim_rocket_singlecore_no_nic/firesim.tar.gz (1.2MB)', 'Tarball contents list correctly shows xilinx_alveo_v80/firesim.pdi and xilinx_alveo_v80/metadata', 'firesim.pdi exists and is non-zero (5.1MB data file)', 'Metadata file has correct comma-separated key:value format with all required fields (buildquintuplet, deployquintuplet, buildtriplet, deploytriplet, commit, buildmakefrag, deploymakefrag)', 'Metadata successfully parsed by firesim_description_to_tags() from awstools/afitools.py', "HWDB entry 'xilinx_alveo_v80_firesim_rocket_singlecore_no_nic' exists in config_hwdb.yaml after DOCREF END marker", "YAML parsing succeeds with 'HWDB entry parsed OK' - bitstream_tar and custom_runtime_config keys present", "RuntimeHWConfig dict[] access simulation passes - no KeyError on hwconfig_dict['custom_runtime_config'] (line 286) or hwconfig_dict['bitstream_tar']", 'HWDB entry uses correct 4-space YAML indentation consistent with midasexamples_gcd entry', 'bitstream_tar uses file:// URI pointing to correct tarball path', 'deploy_quintuplet_override and custom_runtime_config both set to null', 'Runtime config YAML has default_platform: XilinxAlveoV80InstanceDeployManager', 'V80 HWDB entry found in hwdb when cross-referenced from runtime config']
Part 3: ["HWDB entry 'xilinx_alveo_v80_firesim_rocket_singlecore_no_nic' exists in config_hwdb.yaml with bitstream_tar path, deploy_quintuplet_override, and custom_runtime_config fields", "Build recipe 'xilinx_alveo_v80_firesim_rocket_singlecore_no_nic' exists in config_build_recipes.yaml with all 11 required fields (PLATFORM, DESIGN, TARGET_CONFIG, PLATFORM_CONFIG, TARGET_PROJECT, TARGET_PROJECT_MAKEFRAG, deploy_quintuplet, platform_config_args, post_build_hook, metasim_customruntimeconfig, bit_builder_recipe)", "config_runtime.yaml default_hw_config set to 'xilinx_alveo_v80_firesim_rocket_singlecore_no_nic' matching the HWDB entry name", "config_runtime.yaml default_platform set to 'XilinxAlveoV80InstanceDeployManager'", "Build recipe PLATFORM 'xilinx_alveo_v80' matches deploy manager PLATFORM_NAME in run_farm_deploy_managers.py (line 1450)", "Deploy manager class 'XilinxAlveoV80InstanceDeployManager' exists in run_farm_deploy_managers.py (line 1447)", "bit_builder_recipe references 'bit-builder-recipes/xilinx_alveo_v80.yaml' and that file exists on disk", 'Build recipe structure validated against midasexamples_gcd reference entry — all 11 fields present with correct V80-specific values', "Python validation script printed 'ALL CONSISTENCY CHECKS PASSED (9/9)'"]

## Notes


