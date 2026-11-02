# Prompts

Agent role prompts for the FPGA porting workflow. Each file defines what an agent should do, how it should make decisions, and what its scope of responsibility is.

## Files

| File | Role | Description |
|------|------|-------------|
| `orchestrator.md` | Orchestrator | Top-level agent that decomposes the porting task into steps, assigns work, and tracks progress |
| `step-lead.md` | Step Lead | Owns a single porting step end-to-end: plans, delegates implementation, reviews results |
| `impl-and-debug.md` | Implementer/Debugger | Writes code, runs builds, debugs failures. Hands-on execution agent |
| `verifier.md` | Verifier | Validates that a step's output is correct: runs tests, checks constraints, signs off |
| `fpga-<FPGAName>.md` | FPGA Override | Per-FPGA prompt additions that specialize the generic agent prompts for a specific target board |

## Adding a new prompt

1. Create `<role-name>.md` in this directory.
2. Define: role scope, decision authority, what references the agent should consult, and success criteria.
3. Keep technical details (tool usage, specs) in `references/` — prompts should point to references, not duplicate them.
4. Add an entry to the table above.

## FPGA-specific overrides

When porting to a new FPGA, create `fpga-<FPGAName>.md` (e.g., `fpga-XilinxAlveoV80.md`). This file contains prompt additions that are injected alongside the generic role prompts. It should cover:

- Board-specific constraints and gotchas
- Which reference docs are most relevant for this target
- Any deviations from the standard porting flow
