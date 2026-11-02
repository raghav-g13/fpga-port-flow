# Running the Flow

## 1. Environment

```bash
cd $FLOW_DIR
conda activate chia_env
source ~/create-ssh-agent.sh
```

## 2. Start cluster

```bash
python -m chia.cli.main up cluster.yaml
```

## 3. Submit job

```bash
RAY_ADDRESS=$HEAD_IP:6380 chia job submit -- python $FLOW_DIR/fpga_port_flow.py
```

Follow logs:

```bash
RAY_ADDRESS=$HEAD_IP:6380 ray job logs --follow \
  $(RAY_ADDRESS=$HEAD_IP:6380 ray job list --format json 2>/dev/null \
    | python3 -c "import sys,json; jobs=json.load(sys.stdin); print(jobs[0]['submission_id'])")
```

Dashboard: `http://$HEAD_IP:8082`

## 4. Human review gates

The flow blocks until you approve each plan:

```bash
touch out/review/step_plan.approved
touch out/review/step{N}_parts.approved
```

## 5. Tear down

```bash
python -m chia.cli.main down cluster.yaml
```

## Resume

```bash
RAY_ADDRESS=$HEAD_IP:6380 chia job submit -- \
  python $FLOW_DIR/fpga_port_flow.py --resume-step 8 --resume-part 2
```
