# fpga-port-flow

Multi-agent FPGA porting flow for FireSim. Orchestrates Claude Code agents via [Chia](https://github.com/ucb-bar/chia) + Ray to port FireSim to new FPGA platforms.

```
orchestrator → step-lead → impl-and-debug ⇄ verifier → next step
```

## Setup

```bash
git clone --recurse-submodules <this-repo>
conda activate chia_env
```

Set environment variables (add to your shell profile or a local `.env`):

```bash
export FLOW_DIR=/path/to/fpga-port-flow
export HEAD_IP=<cluster-head-hostname>
export VIVADO_DIR=/path/to/xilinx/2025.1
export EDA_DIR=/path/to/eda-tools
export REFERENCES=/path/to/knowledge-base/references
```

The `firesim/` submodule is volume-mounted into the chipyard container at runtime.

## Docker image

```bash
./build.sh    # builds ghcr.io/ucb-bar/chia-v80-chipyard:latest
```

## Run

```bash
python -m chia.cli.main up cluster.yaml
RAY_ADDRESS=$HEAD_IP:6380 chia job submit -- python fpga_port_flow.py
```

Human review gates block at `out/review/`. Approve with:
```bash
touch out/review/step_plan.approved
touch out/review/step{N}_parts.approved
```

Follow logs:
```bash
RAY_ADDRESS=$HEAD_IP:6380 ray job logs --follow <submission_id>
```

Resume from a specific step/part:
```bash
chia job submit -- python fpga_port_flow.py --resume-step 3 --resume-part 2
```

Tear down:
```bash
python -m chia.cli.main down cluster.yaml
```

## Examples

See `examples/` for reference material:
- `porting-steps.md` — the high-level porting steps each agent follows
- `v80-xdma/` — sample commit-db and debug-kb entries for a V80 XDMA port

## Repo structure

```
├── fpga_port_flow.py    # main orchestration script
├── prompts/             # agent system prompts
├── steps/               # step plan JSONs
├── cluster.yaml         # Chia/Ray cluster config
├── firesim/             # submodule: firesim/firesim (mounted into container)
├── commit-db/           # append-only commit database (see commit-db/MANIFEST.md)
├── debug-kb/            # debug knowledge base (see debug-kb/MANIFEST.md)
├── examples/            # porting steps reference + example commit-db/debug-kb entries
│   ├── porting-steps.md
│   └── v80-xdma/
├── build.sh / run.sh    # Docker build and run helpers
└── V80ChipyardDockerfile
```
