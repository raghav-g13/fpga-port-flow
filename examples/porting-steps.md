# Adding a New FPGA to FireSim — High-Level Porting Steps

Source: Adapted from [FireSim docs — Adding FPGAs](https://docs.fires.im/en/latest/Advanced-Usage/Adding-FPGAs.html)

## Agentic porting flow

Each step is tagged with who does the work:

| Tag | Meaning |
|-----|---------|
| **AGENT** | Agent implements, tests, and verifies — writes code, runs builds/simulations, iterates on failures |
| **AGENT → HUMAN TEST** | Agent implements; human runs the result on real FPGA hardware and reports back |

Each step has a **Quirks & Decisions** section. The agent records discoveries, workarounds, and design choices there as it works, persisting them to the FPGA-specific reference file (e.g., `references/fpga/<FPGAName>.md`) under a heading matching the step.

## Prerequisites

The target FPGA must provide:
- **MMIO interface** — 32-bit AXI4-Lite for simulation coordination (primary requirement)
- **DMA interface** — 512-bit AXI4 for bulk data transfer (secondary requirement; needed for TracerV, FASED DDR modeling)
- **DRAM** — on-board memory accessible from the FPGA fabric (secondary requirement; needed for FASED)

For Xilinx platforms, depending on the architecture and the specific FPGA, XDMA or QDMA IP + software libraries typically provide both MMIO and DMA interfaces over PCIe.

---

## Step 1: Platform Scaffolding — AGENT

**Goal:** Set up the platform directory structure, build scripts, constraints, and Scala configuration — everything needed before feature implementation begins.

**Agent implements:**
- `$FIRESIM/platforms/<platform_name>/` — top-level platform directory
- `build-bitstream.sh` — invoked by the build system with `CL_DIR` pointing to the build area; calls Vivado or other synthesis tool
- `cl_firesim/` — directory structure for RTL sources, constraints (XDC), TCL scripts for IP instantiation and synthesis
- Skeleton top-level Verilog/SystemVerilog module with `F1Shim` instantiation and all feature ports tied off
- `$FIRESIM/sim/midas/src/main/scala/midas/Config.scala` — define the top-level module name, AXI4 bus parameters (address/data widths, ID widths), and which ports are available (MMIO, DMA, memory)
- `$FIRESIM/sim/midas/src/main/scala/configs/CompilerConfigs.scala` — specify DRAM configuration (capacity, channels, data width) and port characteristics

**Agent verifies:**
- Directory structure matches the pattern of existing platforms
- Scala compiles cleanly; generated RTL (`F1Shim`) has the expected port signatures
- Skeleton top-level elaborates without errors (all ports tied off)
- `build-bitstream.sh` is syntactically correct and references the right tool paths

**Quirks & Decisions to document:**
- How the FPGA exposes PCIe to the fabric (XDMA IP, QDMA IP, hard block, etc.) and why that choice was made
- Block design (BD) vs pure RTL for PCIe/interconnect/memory plumbing — rationale
- Clocking and reset architecture — clock domains, crossing strategies
- Pin constraints and floorplanning choices
- AXI4 ID widths, address widths, data widths chosen and why
- DRAM channel count and capacity mapping
- Any deviations from existing platform configs and why

**Reference:** Existing platform directories under `$FIRESIM/platforms/` (e.g., `xilinx_alveo_u250`, `xilinx_alveo_u280`) are good templates. You should also refer to documentation specific to the FPGA being ported.

---

## Step 2: FPGA Top and FireSim Wrapper Feature Implementation — AGENT

**Goal:** Incrementally implement the features that the FPGA top-level and FireSim wrapper must provide, connecting `F1Shim` to the board's physical interfaces.

Features are implemented in this order (each builds on the previous):

### 2a. AXI4-Lite MMIO

Connect the 32-bit AXI4-Lite bus from `F1Shim`'s `io_master` port to the FPGA's PCIe interface. This is the primary control path — FireSim uses it for all simulation coordination.

- Wire PCIe BAR → AXI4-Lite → `F1Shim` `io_master`
- DMA and DRAM ports remain tied off

### 2b. AXI4 DMA

Connect the 512-bit AXI4 bus from `F1Shim`'s `io_pcis` port to the FPGA's DMA engine. This enables bulk data transfer (TracerV, faster communication).

- Wire PCIe DMA engine → AXI4 → `F1Shim` `io_pcis`
- DRAM port remains tied off
- Update Scala config if DMA was initially stubbed

### 2c. DRAM Interface

Connect the memory controller to `F1Shim`'s memory port(s). This enables FASED DDR modeling for full system simulation.

- Wire on-board memory (DDR4, HBM, etc.) → memory controller → `F1Shim` memory ports
- Update Scala config for DRAM channel count and capacity
- Configure FASED memory model parameters

**Agent verifies (per feature):**
- RTL elaborates cleanly with the new connections
- Vivado synthesis passes without errors; review critical warnings
- Port widths, ID widths, and address maps match the Scala config

**Quirks & Decisions to document (per feature):**
- IP configurations chosen (XDMA vs QDMA parameters, BAR sizes, queue depths)
- Address map / aperture routing details
- Any synthesis workarounds (IP version pinning, parameter overrides, constraint exceptions)
- Interconnect topology (SmartConnect, NoC, crossbar) and why

---

## Step 3: Simulation & Pre-Silicon Validation — AGENT

**Goal:** Build and run simulation infrastructure to validate each feature from Step 2 before moving on.

**Agent implements:**
- Testbench top-level — instantiates the endpoint design and a PCIe root-port BFM (or equivalent)
- Simulation setup script (TCL or other) — creates the simulation project, sources all files, configures the simulator
- Test programs — one per feature:
  - **2a (MMIO):** BAR read/write test — MMIO transactions through to `F1Shim` `io_master`
  - **2b (DMA):** DMA data movement test — bulk transfers through to `F1Shim` `io_pcis`
  - **2c (DRAM):** Memory read/write test — data through to memory controller and back

**Agent verifies:**
- PCIe link training completes (LTSSM reaches L0)
- Each feature's test passes in simulation
- Address map / aperture routing is correct (data reaches the right destination)

**Quirks & Decisions to document:**
- Simulator chosen (VCS vs XSim) and why — performance differences can be dramatic
- Vendor IP behavioral model limitations (signals that can't be probed, timing artifacts)
- Long initialization phases that look like hangs but are expected (e.g., CDO programming)
- Testbench hierarchy path issues (XMR paths that break when wrapper changes)
- Any workarounds for simulator-specific bugs
- Expected simulation timeline (how long each phase takes in sim time and wall clock)

---

## Steps 2 ↔ 3: Implement-and-Validate Loop

Steps 2 and 3 form a loop. For each feature (2a → 2b → 2c):

```
┌─────────────────────────────────────────────────┐
│  For each feature (MMIO, DMA, DRAM):            │
│                                                 │
│    Step 2: Implement feature in FPGA top        │
│        │                                        │
│        ▼                                        │
│    Step 3: Run simulation tests for feature     │
│        │                                        │
│        ├── PASS → move to next feature          │
│        │                                        │
│        └── FAIL → fix RTL/testbench,            │
│                   re-run simulation              │
│                   (loop until pass)              │
└─────────────────────────────────────────────────┘
```

**Scope of testing in this loop:** Steps 2↔3 validate the **platform hardware plumbing** — PCIe BFM drives TLPs through the FPGA's interconnect into `F1Shim` and back. This confirms the RTL is wired correctly, address maps route to the right destinations, and data moves intact. It does NOT exercise the C++ host driver, FireSim's simulation infrastructure (Golden Gate, MIDAS bridges), or real workloads — those are tested in Step 6 (integration testing with `simif_<platform>` via co-simulation bridge) and Step 8 (real hardware).

The loop exits when all features are implemented and all simulation tests pass cleanly. Only then proceed to Step 4.

---

## Step 4: C++ Host Driver — AGENT

**Goal:** Implement the host-side software that communicates with the FPGA over PCIe for simulation control.

**Agent implements:**
- `$FIRESIM/sim/midas/src/main/cc/simif_<platform>.cc` (and `.h`)
- Functions: `fpga_setup()`, `read()`/`write()` (MMIO), `cpu_managed_axi4_read()`/`write()` (DMA)

**Agent verifies:**
- Driver compiles cleanly against the build system (Step 5)
- Code review against existing drivers for interface conformance

**Quirks & Decisions to document:**
- Linux kernel driver used (XDMA, QDMA, or platform-specific) and why
- PCIe BAR layout — which BAR maps to MMIO vs DMA vs control
- Device file paths (e.g., `/dev/xdma0_user`, `/dev/xdma0_h2c_0`)
- BAR size mismatches between RTL config and driver expectations
- XDMA vs QDMA behavioral differences (interrupt modes, descriptor formats)
- Kernel driver version compatibility issues

---

## Step 5: Build System Integration — AGENT

**Goal:** Wire the new platform into FireSim's Makefile infrastructure so `make` builds both the driver binary and RTL output products.

**Agent implements:**
- `$FIRESIM/sim/make/fpga.mk` — add rules for RTL compilation/synthesis targeting the new platform
- `$FIRESIM/sim/make/driver.mk` — add rules for compiling the C++ driver with correct includes and link flags (conda dependencies, XDMA headers, etc.)

**Agent verifies:**
- `make -C sim PLATFORM=<platform_name> <platform_name>` produces both the simulation driver binary and the generated RTL/IP
- Iterate on build errors until clean

**Quirks & Decisions to document:**
- Non-obvious link dependencies or include paths
- Conda environment requirements
- Any Makefile conditionals or platform-specific flags needed

---

## Step 6: Integration Testing — AGENT

**Goal:** Validate the full FireSim stack end-to-end by running a real workload through both the platform's FPGA simulation and metasimulation. Steps 2↔3 validated individual hardware interfaces with unit-level BFM tests; this step tests everything working together with an actual boot.

The test workload is `bare` (`deploy/workloads/bare.json`) — a baremetal "hello world" that boots, prints to UART, and exits. It uses `common_bootbinary` (FireMarshal bare hello) and `common_rootfs` (dummy), producing a `uartlog` output. This is the simplest possible end-to-end FireSim test.

6a and 6b–6c can proceed in parallel:

### 6a. Metasimulation with Workload

Run the `bare` workload through metasimulation (Verilator or VCS model of the target design using `simif_emul`) — the standard FireSim metasim path, unchanged.

**What this tests:**
- Golden Gate correctly transforms the target design for the new platform config
- MIDAS bridges (UART, block device, etc.) are functional
- FASED memory model configuration is correct
- The FireSim infrastructure (separate from platform plumbing) produces a bootable design

**What this does not test:**
- Platform-specific RTL (PCIe IP, interconnect) — metasim wraps F1Shim directly
- Platform-specific C++ driver (`simif_<platform>`) — metasim uses `simif_emul`

### 6b. Co-Simulation Bridge Setup

`simif_<platform>` natively talks to kernel device files (`/dev/xdma0_*`), but its interface — `read()`/`write()` (MMIO) and `cpu_managed_axi4_read()`/`write()` (DMA) — maps directly to AXI4-Lite and AXI4 transactions. These are exactly the interfaces the FPGA simulation already models. A co-simulation bridge connects the driver to the simulated design, enabling full driver-in-the-loop testing without real hardware.

**Agent implements:**
- Abstract the device-access layer in `simif_<platform>` so it can be backed by either real device files (for hardware) or a simulation backend
- Implement the simulation backend: DPI calls, shared memory, or sockets that translate `read()`/`write()`/DMA operations into AXI transactions on the simulated design's ports
- Bridge connects to the platform top-level's AXI ports (same ones the PCIe BFM drives in Step 3)

### 6c. Full FPGA Simulation with Workload (using co-sim bridge)

Run the `bare` workload through the platform's RTL simulation infrastructure (the testbench from Step 3), with `simif_<platform>` driving the simulated design through the co-simulation bridge from 6b.

**What this tests:**
- Platform-specific C++ driver (`simif_<platform>`) end-to-end against simulated RTL
- Platform-specific RTL under a real workload (not just BFM unit tests)
- PCIe + interconnect behavior during sustained simulation traffic
- Address map routing under realistic access patterns
- Interaction between FASED memory traffic and DMA/MMIO traffic
- Architecture-specific bugs in the platform plumbing (timing, arbitration, backpressure)
- Driver ↔ RTL integration: BAR offsets, data widths, byte ordering, transaction sequencing

### Verification and diagnosis

**Agent verifies (6a and 6c):**
- Simulation completes without hanging or crashing
- `uartlog` contains the expected "hello" output
- No assertion failures or FASED errors in the simulation log
- If 6a passes but 6c fails: bug is in the platform RTL, the driver, or the driver ↔ RTL interface — not in the FireSim infrastructure
- If 6c passes but 6a fails: bug is in the Scala config or Golden Gate transforms — not in the platform plumbing

**Quirks & Decisions to document:**
- Co-simulation mechanism chosen (DPI, shared memory, sockets) and why
- How the device-access abstraction is structured (compile-time vs runtime switching)
- Any latency or synchronization issues between driver and simulation
- Commands used for both simulation types and any platform-specific flags
- Wall-clock time for each (baseline expectation for future runs)
- Any config adjustments needed (e.g., memory size limits for Verilator, simulation timeout tuning)
- Differences in behavior between 6a and 6c and how they were resolved

---

## Step 7: Manager — Bitstream Builder — AGENT

**Goal:** Teach the FireSim manager how to orchestrate bitstream builds for the new platform.

**Agent implements:**
- `$FIRESIM/deploy/buildtools/bitbuilder.py` — add a `BitBuilder` subclass with:
  - `setup()` — prepare the build environment (copy platform directory, inject generated RTL)
  - `build_bitstream()` — invoke `build-bitstream.sh`, package the result
- `$FIRESIM/deploy/bit-builder-recipes/<platform>.yaml` — build parameter recipe (device part, synthesis strategy, etc.)

**Agent verifies:**
- Run `firesim buildbitstream` end-to-end
- Confirm bitstream is generated and packaged correctly
- Check for timing violations in the build report

**Quirks & Decisions to document:**
- Synthesis strategy choices (e.g., performance vs area optimization)
- Any Vivado directives or implementation strategies needed for timing closure
- Build time expectations
- Bitstream packaging format differences from other platforms

**Build flow orchestrated by the manager:**
1. Golden Gate generates `FireSim-generated.sv` from the design specification
2. Manager copies `cl_firesim/` to the build farm with a unique name
3. Generated RTL is placed into the copied platform directory
4. `build-bitstream.sh` executes synthesis + implementation + bitstream generation
5. Resulting bitstream is packaged and registered in the HWDB

---

## Step 8: Configuration & HWDB Registration — AGENT

**Goal:** Create the runtime configuration files that let users select and use the new platform.

**Agent implements:**
- Runtime config YAML — set `default_platform` to the new `InstanceDeployManager` class
- HWDB entry — register the built bitstream with metadata (platform, design config, bitstream path)
- Any platform-specific config knobs (clock frequencies, memory sizes, feature flags)

**Agent verifies:**
- Config files parse correctly
- HWDB entry references valid bitstream paths from Step 7
- Manager commands (`firesim managerinit`, `firesim buildbitstream`) accept the new config without errors

**Quirks & Decisions to document:**
- Any non-obvious config knob values and why they were chosen
- Deviations from default config templates

---

## Step 9: Manager — Runtime & Deployment — AGENT → HUMAN TEST

**Goal:** Teach the FireSim manager how to flash the FPGA, deploy simulation collateral, and run simulations on the new platform.

**Why human testing is needed:** Flashing an FPGA, PCIe re-enumeration, and end-to-end deployment require physical access to a server with the target FPGA installed.

**Agent implements:**
- `$FIRESIM/deploy/firesim` — register the platform for `firesim managerinit`
- `$FIRESIM/deploy/runtools/run_farm_deploy_managers.py` — implement `InstanceDeployManager` subclass:
  - FPGA flashing procedure (how to load the bitstream onto the device)
  - Simulation directory creation
  - Collateral deployment (driver binary, disk images, etc.)
  - PCIe re-enumeration or warm-reset after flashing

**Human tests on FPGA server and reports back:**
- Flash a bitstream using the deploy manager — does programming succeed?
- PCIe re-enumeration — does the device reappear after flashing? Any `dmesg` errors?
- `firesim infrasetup` → `firesim runworkload` — does the full flow complete?
- Report failures, logs, and `dmesg` output back to agent for fixes

**Prerequisites from other tracks:** Human testing requires the driver binary (from Step 5), the bitstream (from Step 7), and the config/HWDB entry (from Step 8). Both left and right tracks must complete before the human can test end-to-end.

**Quirks & Decisions to document:**
- Flashing tool and invocation (e.g., `vivado -mode batch`, vendor-specific programmer)
- PCIe re-enumeration method (e.g., `pci_rescan`, hot-reset scripts, `setpci`)
- Whether full-bitstream programming drops PCIe and how to recover
- Any sudo or permissions requirements for flashing
- Timing constraints (how long flashing takes, cool-down periods)

**Key consideration for full-bitstream platforms:** Unlike AWS F1 (partial reconfiguration with a preserved shell), full-bitstream programming temporarily takes down PCIe. The deploy manager must handle re-enumeration or use a workaround (e.g., `pci_rescan`, hot-reset scripts).

---

## Dependency graph

```
Step 1 (Scaffolding)
    │
    ▼
┌──────────────────────────┐
│  Step 2 ↔ 3 Loop         │
│  (Feature Impl + Sim)    │
│  2a MMIO → sim → pass    │
│  2b DMA  → sim → pass    │
│  2c DRAM → sim → pass    │
└──────────┬───────────────┘
           │
     ┌─────┴──────────┐
     ▼                ▼
Step 4             Step 7 (BitBuilder)
(Driver)              │
     │                ▼
     ▼             Step 8 (Config/HWDB)
Step 5                │
(Build System)        │
     │                │
     ├────────────────┤
     ▼                ▼
┌─── Step 6 ────┐  Step 9 (Runtime/Deploy) ← only HUMAN TEST step
│               │     ▲
│ 6a ║ 6b→6c   │     │ also needs driver binary (Step 5)
│    ║         │     │ and bitstream (Step 7)
│ Both pass    │
└──────────────┘
```

Steps 1 → 2/3 loop is the core RTL development cycle. After the loop, two tracks proceed in parallel:
- **Left track:** Steps 4 → 5 → 6 — driver, build system, then integration testing.
- **Right track:** Steps 7 → 8 — bitstream builder, then config/HWDB registration.
- **Within Step 6:** 6a (metasim, standard path) runs in parallel with 6b → 6c (co-sim bridge setup, then full FPGA sim with driver-in-the-loop). Both must pass.
- **Step 9 (Runtime/Deploy)** depends on both tracks: it needs the driver binary from Step 5, the bitstream from Step 7, and the config from Step 8. This is the only step requiring human testing on real hardware; all others are fully agent-driven.
