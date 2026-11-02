# V80-Specific Agent Guidance

When porting to the Xilinx Alveo V80, all agents should keep the following in mind:

## Design philosophy

We are **actively avoiding the AVED (Alveo Versal Example Design) flow**. The goal is a simple, Vivado-based flow consistent with how existing Alveo and Corigine platforms work in FireSim. AVED repos and docs are useful for learning how the V80 hardware works, but should not be adopted as the build/deploy framework.

## Key references

- Board details and links: `/nscratch/raghavgupta/fpga-port/references/fpga/XilinxAlveoV80.md`
- XSim simulation setup: `/nscratch/raghavgupta/fpga-port/references/tools/vivado-xsim.md`
- Environment setup: `/nscratch/raghavgupta/fpga-port/references/firesim/environment.md`
- Platform source: `$FIRESIM/platforms/xilinx_alveo_v80/`

## Container specifics

- Vivado 2025.1 is available at `/ecad/tools/xilinx/2025.1/` (bind-mounted read-only from host)
- The V80 container image (`chia-v80-chipyard`) is built from the `fpga-ports` branch of chipyard, which includes V80 platform scaffolding
- FireSim is volume-mounted from the host at `$FIRESIM` — changes persist across container restarts
