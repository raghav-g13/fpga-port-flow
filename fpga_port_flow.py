"""
V80 FPGA porting flow.

Orchestrates the multi-agent FPGA porting workflow:
  orchestrator → step-lead → impl-and-debug ⇄ verifier → next step

Python controls all routing. LLM agents return structured JSON;
no agent-to-agent communication.

Usage:
    python -m chia.cli.main up cluster.yaml
    chia job submit -- python fpga_port_flow.py
    python -m chia.cli.main down cluster.yaml
"""

import json
import logging
import re
import shlex
import sys
import time
from pathlib import Path

import ray
from chia.base.ChiaFunction import ChiaFunction, get
from chia.base.tools.BashTool import BashTool
from chia.base.tools.AsyncBashTool import AsyncBashTool
from chia.models.claude import ClaudeCodeLLM

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CHIPYARD_PATH = "/home/ray/chipyard"

CHIPYARD_TOOL_RESOURCE = 0.01
LLM_RESOURCE = 1.0

MAX_IMPL_ATTEMPTS = 5
PORT_BRANCH = "fpga-port/v80"

FLOW_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = FLOW_DIR / "prompts"
PORTING_STEPS_REF = str(FLOW_DIR / "examples" / "porting-steps.md")
RUNTIME_ENV = {
    "working_dir": str(FLOW_DIR),
    "py_modules": [],
    "excludes": ["out/", "__pycache__", ".mypy_cache", "firesim/"],
}

LLM_MODEL = "claude-opus-4-6"
DEFAULT_LLM_TIMEOUT = 1800

logger = logging.getLogger("fpga_port_flow")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)


REVIEW_BASE = FLOW_DIR / "out" / "review"
REVIEW_POLL_INTERVAL = 10  # seconds


def wait_for_human_review(review_dir: Path, name: str, data: dict) -> dict:
    """Write *data* to a JSON file and block until the human approves.

    Files are kept after approval for auditability.
    """
    review_dir.mkdir(parents=True, exist_ok=True)
    json_path = review_dir / f"{name}.json"
    approved_path = review_dir / f"{name}.approved"

    # Clean stale signals from a previous run with the same run_id
    approved_path.unlink(missing_ok=True)

    json_path.write_text(json.dumps(data, indent=2))
    logger.info("=" * 60)
    logger.info("HUMAN REVIEW REQUIRED: %s", name)
    logger.info("  Review / edit: %s", json_path)
    logger.info("  When ready:    touch %s", approved_path)
    logger.info("=" * 60)

    while not approved_path.exists():
        time.sleep(REVIEW_POLL_INTERVAL)

    reviewed = json.loads(json_path.read_text())
    logger.info("Human approved %s — continuing", name)
    return reviewed


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.md").read_text()


def extract_json(text: str) -> dict:
    """Extract the last ```json``` fenced block, or the last bare JSON object."""
    matches = re.findall(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if matches:
        return json.loads(matches[-1])
    brace_depth = 0
    start = None
    last_json = None
    for i, c in enumerate(text):
        if c == "{":
            if brace_depth == 0:
                start = i
            brace_depth += 1
        elif c == "}":
            brace_depth -= 1
            if brace_depth == 0 and start is not None:
                try:
                    last_json = json.loads(text[start : i + 1])
                except json.JSONDecodeError:
                    pass
                start = None
    if last_json is not None:
        return last_json
    raise ValueError(f"No JSON found in LLM response:\n{text[:500]}")


# ---------------------------------------------------------------------------
# Git + commit-database helpers
# ---------------------------------------------------------------------------

COMMIT_DB = FLOW_DIR / "commit-db"
FIRESIM_PATH = f"{CHIPYARD_PATH}/sims/firesim"

REPOS = {
    "FIRESIM": FIRESIM_PATH,
    "CHIPYARD": CHIPYARD_PATH,
}


@ChiaFunction(resources={"chipyard": 0.01})
def _run_on_chipyard(cmd: str) -> str:
    import subprocess
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
    out = r.stdout
    if r.stderr:
        out += "\nSTDERR:\n" + r.stderr
    if r.returncode != 0:
        out += f"\n[exit code: {r.returncode}]"
    return out


_GIT_SAFE_ENV = (
    "export GIT_CONFIG_COUNT=2 "
    "GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0=/home/ray/chipyard/sims/firesim "
    "GIT_CONFIG_KEY_1=safe.directory GIT_CONFIG_VALUE_1=/home/ray/chipyard"
)


def _git(repo_path: str, cmd: str) -> str:
    return get(_run_on_chipyard.chia_remote(
        f"{_GIT_SAFE_ENV} && cd {repo_path} && git {cmd}"
    ))


def _git_head(repo_path: str) -> str:
    out = _git(repo_path, "rev-parse HEAD")
    for line in out.strip().split("\n"):
        line = line.strip()
        if re.fullmatch(r"[0-9a-f]{7,40}", line):
            return line
    raise ValueError(f"rev-parse HEAD returned no hash: {out!r}")


def _git_has_changes(repo_path: str) -> bool:
    out = _git(repo_path, "status --porcelain -- . ':!platforms/f1/aws-fpga'")
    return bool(out.strip().split("\n")[0].strip())


class RepoState:
    """Tracks git state for one repo."""

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.base_hash: str = ""

    def create_branch(self):
        _git(self.path, f"checkout -B {PORT_BRANCH}")
        self.base_hash = _git_head(self.path)
        logger.info("[%s] on branch %s at %s", self.name, PORT_BRANCH, self.base_hash[:12])

    def head(self) -> str:
        return _git_head(self.path)

    def has_changes(self) -> bool:
        return _git_has_changes(self.path)

    def diff_from(self, commit_hash: str) -> str:
        return _git(self.path, f"diff {commit_hash} HEAD -- . ':!platforms/f1/aws-fpga'")

    def commit(self, message: str) -> str:
        _git(self.path, f"add -A -- . ':!platforms/f1/aws-fpga' && git commit -m {shlex.quote(message)}")
        return self.head()

    def reset_to(self, commit_hash: str):
        _git(self.path, f"reset --hard {commit_hash}")
        logger.info("[%s] reset to %s", self.name, commit_hash[:12])


class MultiRepoManager:
    """Manages git across chipyard and firesim repos together."""

    def __init__(self):
        self.repos = {
            name: RepoState(name, path) for name, path in REPOS.items()
        }

    def create_branches(self):
        for r in self.repos.values():
            r.create_branch()

    def snapshot(self) -> dict[str, str]:
        """Capture HEAD of each repo as a rollback point."""
        return {name: r.head() for name, r in self.repos.items()}

    def reset_to(self, snapshot: dict[str, str]):
        for name, commit_hash in snapshot.items():
            self.repos[name].reset_to(commit_hash)

    def commit_all(self, message: str) -> dict[str, str]:
        """Commit in each repo that has changes. Returns {repo: hash}."""
        hashes = {}
        for name, r in self.repos.items():
            if r.has_changes():
                hashes[name] = r.commit(f"[{name}] {message}")
                logger.info("[%s] committed %s", name, hashes[name][:12])
        return hashes

    def diff_all(self, snapshot: dict[str, str]) -> dict[str, str]:
        """Get diffs from snapshot for each repo."""
        diffs = {}
        for name, commit_hash in snapshot.items():
            d = self.repos[name].diff_from(commit_hash)
            if d.strip():
                diffs[name] = d
        return diffs


def write_commit_file(
    repo: str, step_id: int, part_id: int, iter_num: int,
    parent: str, summary: str, message: str,
    diff: str, files_modified: list[str],
    commit_hash: str,
):
    """Write a commit file to the commit database per MANIFEST schema."""
    from datetime import datetime, timezone
    commit_id = f"{repo}-STEP{step_id}-PART{part_id}-ITER{iter_num}"
    step_dir = COMMIT_DB / f"step{step_id}"
    step_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(timezone.utc).isoformat()
    files_section = "\n".join(f"- `{f}`" for f in files_modified) or "- (none)"

    content = f"""\
---
id: {commit_id}
repo: {repo}
step: {step_id}
part: {part_id}
iter: {iter_num}
parent: {parent}
timestamp: {ts}
git_hash: {commit_hash}
---

# {summary}

## Message

{message}

## Diff

```diff
{diff}
```

## Files modified

{files_section}
"""
    (step_dir / f"{commit_id}.md").write_text(content)
    logger.info("Wrote commit %s", commit_id)
    return commit_id


def write_checkpoint(
    step_id: int, commit_ids: list[str], verification: str, notes: str = "",
):
    """Write an active checkpoint for a step, superseding any existing one."""
    import uuid
    from datetime import datetime, timezone

    step_dir = COMMIT_DB / f"step{step_id}"
    step_dir.mkdir(parents=True, exist_ok=True)

    cp_id = f"step{step_id}-{uuid.uuid4().hex[:8]}"

    for f in step_dir.glob(f"step{step_id}-*.md"):
        text = f.read_text()
        if "status: active" in text:
            new_text = text.replace(
                "status: active", f"status: superseded\nsuperseded_by: {cp_id}"
            )
            f.write_text(new_text)
            logger.info("Superseded checkpoint %s", f.name)
    ts = datetime.now(timezone.utc).isoformat()
    seq = "\n".join(f"{i+1}. `{c}`" for i, c in enumerate(commit_ids))

    content = f"""\
---
step: {step_id}
id: {cp_id}
status: active
created: {ts}
---

# Step {step_id} checkpoint

## Commit sequence

{seq}

## Verification

{verification}

## Notes

{notes}
"""
    (step_dir / f"{cp_id}.md").write_text(content)
    logger.info("Created checkpoint %s", cp_id)
    return cp_id


def call_llm(llm, prompt: str, tools=None):
    result = get(
        llm.prompt.options(resources={"llm": LLM_RESOURCE}).chia_remote(
            llm, prompt, tools or []
        )
    )
    if not result.success:
        logger.error("LLM call failed: %s", result.stderr)
    return result


LOG_DIR = str(FLOW_DIR / "debug-kb" / "logs")


def make_llm(system_prompt: str, resume: bool = False, timeout: int = DEFAULT_LLM_TIMEOUT, name: str = "claude_code") -> ClaudeCodeLLM:
    return ClaudeCodeLLM(
        model=LLM_MODEL,
        system_message=system_prompt,
        timeout_seconds=timeout,
        resume_session=resume,
        extra_cli_args=["--effort", "max"],
        log_dir=LOG_DIR,
        logging_name=name,
    )


# ---------------------------------------------------------------------------
# Agent calls
# ---------------------------------------------------------------------------

def call_orchestrator(
    llm: ClaudeCodeLLM, fpga_name: str, tools: list
) -> list[dict]:
    prompt = f"""\
Decompose the FPGA porting task for {fpga_name} into ordered steps.

Read the porting steps reference at {PORTING_STEPS_REF} and the FPGA-specific
guidance in your system prompt.

Before planning, use chipyard_bash to inspect the current state of the port:
- List existing platform files: ls -R $FIRESIM/platforms/xilinx_alveo_v80/
- Check git log for prior work: cd $FIRESIM && git log --oneline -20
- Check chipyard git log: cd $CHIPYARD && git log --oneline -20
- Look at what configs exist, what builds, what doesn't

Then produce steps that account for what is already done vs. what remains.

Respond with a JSON block:
```json
{{
    "steps": [
        {{
            "id": 1,
            "name": "short step name",
            "description": "what this step accomplishes",
            "success_criteria": ["criterion 1", "criterion 2"]
        }}
    ]
}}
```"""
    result = call_llm(llm, prompt, tools=tools)
    return extract_json(result.result)["steps"]


def call_step_lead(
    llm: ClaudeCodeLLM, step: dict, tools: list
) -> list[dict]:
    prompt = f"""\
You are assigned this porting step:

**Step {step['id']}: {step['name']}**
{step['description']}

Success criteria:
{json.dumps(step['success_criteria'], indent=2)}

Use chipyard_bash to inspect the codebase, then break this step into
concrete implementation parts.

Respond with a JSON block:
```json
{{
    "parts": [
        {{
            "id": 1,
            "description": "what to implement",
            "files_to_modify": ["$FIRESIM/path/to/file"],
            "build_command": "command that should succeed when done",
            "done_when": "observable success criterion"
        }}
    ]
}}
```"""
    result = call_llm(llm, prompt, tools)
    return extract_json(result.result)["parts"]


def call_impl(
    llm: ClaudeCodeLLM,
    step: dict,
    part: dict,
    feedback: str | None,
    tools: list,
) -> dict:
    prompt = f"""\
Implement this part of step "{step['name']}":

**Part {part['id']}: {part['description']}**

Files to modify: {json.dumps(part.get('files_to_modify', []))}
Build command: {part.get('build_command', 'N/A')}
Done when: {part.get('done_when', 'N/A')}
"""
    if feedback:
        prompt += f"""
**Verifier feedback from previous attempt — fix the issues below:**
{feedback}
"""
    prompt += """
When done, respond with a JSON block:
```json
{
    "status": "success" or "failed",
    "changes_summary": "what was changed and why",
    "files_modified": ["list of files"],
    "build_output_snippet": "last ~20 lines of build output"
}
```"""
    result = call_llm(llm, prompt, tools)
    try:
        return extract_json(result.result)
    except ValueError:
        return {
            "status": "failed",
            "changes_summary": result.result[:1000],
            "files_modified": [],
            "build_output_snippet": "",
        }


def call_verifier(
    llm: ClaudeCodeLLM,
    step: dict,
    part: dict,
    impl_result: dict,
    tools: list,
) -> dict:
    prompt = f"""\
Verify the implementation of step "{step['name']}", part {part['id']}:

**Part: {part['description']}**
Done when: {part.get('done_when', 'N/A')}

**Implementation report:**
Status: {impl_result.get('status', 'unknown')}
Changes: {impl_result.get('changes_summary', 'N/A')}
Files modified: {json.dumps(impl_result.get('files_modified', []))}

Step success criteria:
{json.dumps(step.get('success_criteria', []), indent=2)}

Run verification commands. Use chipyard_bash for quick checks,
chipyard_async_bash for builds or simulations.

Respond with a JSON block:
```json
{{
    "pass": true or false,
    "checks_performed": ["what you checked"],
    "feedback": "what needs fixing (only if pass is false)"
}}
```"""
    result = call_llm(llm, prompt, tools)
    try:
        return extract_json(result.result)
    except ValueError:
        return {
            "pass": False,
            "checks_performed": [],
            "feedback": f"Could not parse verifier response: {result.result[:500]}",
        }


# ---------------------------------------------------------------------------
# Main flow
# ---------------------------------------------------------------------------

def run_flow(
    fpga_name: str = "Xilinx Alveo V80",
    resume_step_id: int = 0,
    resume_part_id: int = 0,
    review_dir_override: str | None = None,
):
    """Run the porting flow.

    Args:
        resume_step_id: Skip all steps before this ID and all parts before
            resume_part_id within this step.  When non-zero, the step plan
            and per-step parts are loaded from existing review files instead
            of calling the orchestrator / step-lead LLMs.
        resume_part_id: Within resume_step_id, skip parts before this ID.
        review_dir_override: Path to an existing review directory to load
            plans/parts from.  When None a new timestamped directory is
            created (normal mode) or REVIEW_BASE is used (resume mode).
    """
    from datetime import datetime, timezone
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    resuming = resume_step_id > 0

    if review_dir_override:
        review_dir = Path(review_dir_override)
    elif resuming:
        review_dir = REVIEW_BASE
    else:
        review_dir = REVIEW_BASE / run_id

    ray.init(address="auto", runtime_env=RUNTIME_ENV)
    logger.info("Connected to Ray cluster (run_id=%s, resume=%s)", run_id, resuming)
    if resuming:
        logger.info("Resuming from step %d part %d", resume_step_id, resume_part_id)

    # -- Deploy tools --
    chipyard_bash = BashTool(
        name="chipyard_bash",
        work_dir=CHIPYARD_PATH,
        timeout_seconds=600,
        task_options={"resources": {"chipyard": CHIPYARD_TOOL_RESOURCE}},
    )
    chipyard_async_bash = AsyncBashTool(
        name="chipyard_async_bash",
        work_dir=CHIPYARD_PATH,
        task_options={"resources": {"chipyard": CHIPYARD_TOOL_RESOURCE}},
    )
    logger.info("Tools deployed")

    orchestrator_tools = [chipyard_bash]
    step_lead_tools = [chipyard_bash]
    impl_tools = [chipyard_bash, chipyard_async_bash]
    verifier_tools = [chipyard_bash, chipyard_async_bash]

    # -- Load and assemble prompts --
    fpga_override = load_prompt("fpga-XilinxAlveoV80")

    def full_prompt(role: str) -> str:
        return load_prompt(role) + "\n\n" + fpga_override

    orchestrator_sys = full_prompt("orchestrator")
    step_lead_sys = full_prompt("step-lead")
    impl_sys = full_prompt("impl-and-debug")
    verifier_sys = full_prompt("verifier")

    # -- Git setup --
    git = MultiRepoManager()
    git.create_branches()

    # -- Phase 1: decompose --
    if resuming:
        plan_path = review_dir / "step_plan.json"
        logger.info("Resume: loading step plan from %s", plan_path)
        steps = json.loads(plan_path.read_text())["steps"]
    else:
        logger.info("Phase 1: orchestrator decomposing porting task")
        orchestrator_llm = make_llm(orchestrator_sys, name="orchestrator")
        steps = call_orchestrator(orchestrator_llm, fpga_name, orchestrator_tools)
        reviewed = wait_for_human_review(review_dir, "step_plan", {"steps": steps})
        steps = reviewed["steps"]
    logger.info("Proceeding with %d steps", len(steps))

    # -- Phase 2: execute steps sequentially --
    progress = []

    for step in steps:
        step_id = step["id"]

        if resuming and step_id < resume_step_id:
            logger.info("Skipping step %d (before resume point)", step_id)
            continue

        logger.info("=" * 60)
        logger.info("Step %d: %s", step_id, step["name"])
        logger.info("=" * 60)

        # Load parts: from review file if it exists (resume or re-run),
        # otherwise call the step-lead LLM and do human review.
        parts_path = review_dir / f"step{step_id}_parts.json"
        if parts_path.exists():
            logger.info("Loading parts from %s", parts_path)
            parts = json.loads(parts_path.read_text())["parts"]
        else:
            sl_llm = make_llm(step_lead_sys, resume=True, timeout=36000, name=f"step_lead_s{step_id}")
            parts = call_step_lead(sl_llm, step, step_lead_tools)
            logger.info("Step lead produced %d parts", len(parts))
            reviewed = wait_for_human_review(
                review_dir, f"step{step_id}_parts",
                {"step": step, "parts": parts},
            )
            parts = reviewed["parts"]
        logger.info("Proceeding with %d parts", len(parts))

        step_record = {"step": step, "parts": []}
        step_commit_ids = []
        step_verification = []

        for part in parts:
            if resuming and step_id == resume_step_id and part["id"] < resume_part_id:
                logger.info("Skipping part %d (before resume point)", part["id"])
                continue

            logger.info("--- Part %d: %s", part["id"], part["description"])

            impl_llm = make_llm(impl_sys, resume=True, timeout=10800, name=f"impl_s{step['id']}_p{part['id']}") # 3 hours
            ver_llm = make_llm(verifier_sys, timeout=7200, name=f"verifier_s{step['id']}_p{part['id']}") # 2 hours

            # Rollback point: snapshot HEAD of each repo
            part_base = git.snapshot()
            prev_commit_id = step_commit_ids[-1] if step_commit_ids else "BASE"

            feedback = None
            passed = False
            impl_result = {}
            verdict = {}

            for attempt in range(1, MAX_IMPL_ATTEMPTS + 1):
                logger.info("  Attempt %d/%d", attempt, MAX_IMPL_ATTEMPTS)

                if attempt > 1:
                    git.reset_to(part_base)

                impl_result = call_impl(
                    impl_llm, step, part, feedback, impl_tools
                )
                logger.info(
                    "  Impl status: %s", impl_result.get("status", "unknown")
                )

                if impl_result.get("status") == "failed":
                    feedback = (
                        "Implementation self-reported failure:\n"
                        + impl_result.get("changes_summary", "")
                    )
                    logger.warning("  Impl self-reported failure, retrying")
                    continue

                verdict = call_verifier(
                    ver_llm, step, part, impl_result, verifier_tools
                )
                logger.info("  Verifier: %s", "PASS" if verdict.get("pass") else "FAIL")

                if verdict.get("pass"):
                    passed = True
                    break

                feedback = verdict.get(
                    "feedback", "Verification failed — no details provided."
                )

            # -- Commit management --
            if passed:
                commit_msg = (
                    f"step{step['id']}/part{part['id']}: "
                    f"{impl_result.get('changes_summary', part['description'])[:200]}"
                )
                hashes = git.commit_all(commit_msg)
                diffs = git.diff_all(part_base)

                # One commit-db entry per repo that had changes
                for repo_name, commit_hash in hashes.items():
                    commit_id = write_commit_file(
                        repo=repo_name,
                        step_id=step["id"],
                        part_id=part["id"],
                        iter_num=attempt,
                        parent=prev_commit_id,
                        summary=commit_msg,
                        message=impl_result.get("changes_summary", ""),
                        diff=diffs.get(repo_name, ""),
                        files_modified=impl_result.get("files_modified", []),
                        commit_hash=commit_hash,
                    )
                    step_commit_ids.append(commit_id)
                    prev_commit_id = commit_id

                step_verification.append(
                    f"Part {part['id']}: {verdict.get('checks_performed', [])}"
                )
            else:
                git.reset_to(part_base)
                logger.error(
                    "Part %d FAILED after %d attempts, rolled back",
                    part["id"], MAX_IMPL_ATTEMPTS,
                )

            status = "PASS" if passed else "FAIL"
            logger.info("  Part %d: %s (%d attempts)", part["id"], status, attempt)

            step_record["parts"].append(
                {
                    "part": part,
                    "passed": passed,
                    "attempts": attempt,
                    "impl_result": impl_result,
                    "verdict": verdict,
                }
            )

        # -- Step checkpoint --
        step_ok = all(p["passed"] for p in step_record["parts"])
        if step_ok and step_commit_ids:
            write_checkpoint(
                step_id=step["id"],
                commit_ids=step_commit_ids,
                verification="\n".join(step_verification),
            )

        progress.append(step_record)
        logger.info(
            "Step %d: %s", step["id"], "COMPLETE" if step_ok else "HAS FAILURES"
        )

    # -- Final report --
    report = {
        "fpga": fpga_name,
        "steps": [
            {
                "id": sr["step"]["id"],
                "name": sr["step"]["name"],
                "passed": all(p["passed"] for p in sr["parts"]),
                "parts": [
                    {
                        "id": p["part"]["id"],
                        "description": p["part"]["description"],
                        "passed": p["passed"],
                        "attempts": p["attempts"],
                    }
                    for p in sr["parts"]
                ],
            }
            for sr in progress
        ],
    }

    out_dir = FLOW_DIR / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "flow_report.json"
    report_path.write_text(json.dumps(report, indent=2))
    logger.info("Report: %s", report_path)

    logger.info("=" * 60)
    for s in report["steps"]:
        logger.info(
            "  Step %d (%s): %s", s["id"], s["name"], "PASS" if s["passed"] else "FAIL"
        )
    logger.info("=" * 60)

    chipyard_bash.stop()
    chipyard_async_bash.stop()
    return report


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="V80 FPGA porting flow")
    parser.add_argument("--fpga", default="Xilinx Alveo V80")
    parser.add_argument("--resume-step", type=int, default=0,
                        help="Resume from this step ID (skip earlier steps)")
    parser.add_argument("--resume-part", type=int, default=0,
                        help="Within resume step, skip parts before this ID")
    parser.add_argument("--review-dir", default=None,
                        help="Path to existing review directory with plans/parts")
    args = parser.parse_args()
    run_flow(args.fpga, args.resume_step, args.resume_part, args.review_dir)
