# FPGA Port Commit Database

Append-only commit database for tracking agentic FPGA porting workflows. Each commit records a message and diff; commits form per-step linked lists anchored by checkpoint files.

## Structure

```
commit-db/
├── MANIFEST.md
├── step1/
│   ├── FIRESIM-STEP1-PART1-ITER1.md   # Commit file
│   ├── FIRESIM-STEP1-PART1-ITER2.md
│   ├── CHIPYARD-STEP1-PART2-ITER1.md
│   └── step1-<UUID>.md                 # Checkpoint file
├── step2/
│   └── ...
└── ...
```

## Commit ID scheme

```
<REPO>-STEP<N>-PART<M>-ITER<K>
```

| Component | Meaning |
|-----------|---------|
| `REPO` | Repository prefix — uppercase short name (e.g., `FIRESIM`, `CHIPYARD`) |
| `STEP<N>` | High-level porting step number |
| `PART<M>` | Sub-task within the step |
| `ITER<K>` | Iteration counter, starts at 1 |

### Repo prefixes

| Prefix | Repository |
|--------|------------|
| `FIRESIM` | `$FIRESIM` |
| `CHIPYARD` | `$CHIPYARD` |

## Commit file template

```markdown
---
id: <REPO>-STEP<N>-PART<M>-ITER<K>
repo: <REPO>
step: <N>
part: <M>
iter: <K>
parent: <parent commit ID or BASE>
timestamp: <ISO 8601>
---

# <one-line summary>

## Message

<description of what this commit does and why>

## Diff

\```diff
<unified diff>
\```

## Files modified

- `<path/to/file>`: <what changed>
```

### Parent field

- First commit of a step: `parent: BASE`
- Subsequent commits: point to previous commit in the part
- First commit of a new part: point to last commit of previous part
- Cross-step linkage: handled by checkpoints, not parent pointers

## Checkpoint file template

Filename: `step<N>-<UUID>.md`

```markdown
---
step: <N>
id: step<N>-<UUID>
status: active | superseded
created: <ISO 8601>
superseded_by: <checkpoint ID, only if superseded>
---

# Step <N> checkpoint: <short description>

## Commit sequence

1. `FIRESIM-STEP1-PART1-ITER1`
2. ...

## Verification

<how this step was verified>

## Notes

<context about this attempt>
```

### Checkpoint rules

- Exactly one checkpoint per step may have `status: active` at any time.
- When reimplemented, the old active checkpoint becomes `superseded`.

## Conventions

- Use path variables (`$FIRESIM`, `$CHIPYARD`) — never hardcode absolute paths.
- Commit files are **immutable** once written.
- Checkpoint files may only be modified to change `status` and add `superseded_by`.
