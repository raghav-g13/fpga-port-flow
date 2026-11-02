# FPGA Port Debug Knowledge Base

Implementation-level debug knowledge base for agentic FPGA porting workflows. Stores concrete bugs, errors, and their fixes.

## Structure

```
debug-kb/
├── MANIFEST.md
├── firesim/          # Bugs in FireSim framework code, build system, drivers
├── fpga/             # FPGA platform-specific bugs — board/IP/constraint issues
│   └── <FPGAName>/
└── tools/            # Tool-specific bugs — Vivado, XSim, VCS, etc.
    └── <ToolName>/
```

## Classification

Use the **root cause** to determine category:

- FireSim-generated constraint causes Vivado crash → `firesim/`
- Vivado version bug → `tools/vivado/`
- FPGA IP misconfiguration → `fpga/<FPGAName>/`

## Bug file template

```markdown
# <Short descriptive title>

## Classification

- **Category**: firesim | fpga | tool
- **Target**: <FPGA board or tool name>
- **Porting step**: <step number, if applicable>
- **Severity**: blocker | major | minor
- **Status**: open | resolved | workaround

## Environment

- **FireSim commit/version**: <hash or version>
- **Tool version**: <e.g., Vivado 2025.1>

## Trigger

\```bash
<command(s) that trigger the error>
\```

## Error

\```
<exact error output>
\```

## Root cause

<What is actually wrong and why>

## Resolution

<What was changed to fix it>

### Files modified

- `<path/to/file>`: <what was changed>

## Related

- <Links to related entries>
```

## Conventions

- Use path variables (`$FIRESIM`, `$CHIPYARD`, `$VIVADO_DIR`) — never hardcode paths.
- One bug per file unless tightly coupled.
- Check for duplicates before creating new entries.
