# PyPTO integration

Use Model Harness alongside a target checkout of
[pypto-lib](https://github.com/hw-native-sys/pypto-lib). This guide maps generic
requirements to the project's owning files; it does not duplicate its DSL style
or provide its runtime, device queue or goal host.

## Read the target checkout

Before model work, read `AGENTS.md`, `.claude/CLAUDE.md` and
`.claude/rules/models.md` in that checkout. Follow its task-relevant rules and
skills, including setup, kernel formatting and problem handling. Use the actual
files in the selected checkout as the source of concrete commands and APIs.

| Need | Owning target-project guidance |
| --- | --- |
| Kernel syntax and composition | `docs/pypto-coding/` |
| Setup and toolchain pins | `.claude/skills/setup-env/SKILL.md`, `docs/get-started/installation.md` |
| Kernel style | `.claude/skills/fmt-coding-style/SKILL.md` |
| Numerical execution and comparison | `golden/`, `docs/run-and-validate/golden-harness.md` |
| Compile and generated artifacts | `docs/run-and-validate/compile-runtime-workflow.md` |
| Compiler/runtime diagnosis | `.claude/rules/problem-handling.md`, `docs/debug-and-tune/debugging.md` |
| CI entry discovery | `.github/scripts/detect_changes.py`, `.github/ci_platforms.json` |

Supply the installed `task-submit` skill or the environment's documented queue
workflow for every NPU execution. Do not run hardware jobs directly or invent
missing queue commands. Keep queue configuration and device IDs local.

## Map the execution contract

Complete-model prefill/decode normally live at
`models/<model>/prefill_fwd.py` and `models/<model>/decode_fwd.py`. Compiled
orchestration must cover embedding, all agreed layers, final norm and output
head. Host tokenization, sampling and per-forward generation loops are allowed;
Python per-operator submissions are not a complete compiled forward.

Inspect generated IR/task graphs and effective token shapes, including expanded
helper calls. A compiled token loop around the entire decoder stack fails the
default prefill contract. Necessary recurrence and token tiling remain allowed.
Sparse expert checks include repeated-expert inputs and receive capacity for the
actual dispatched token tile, with real cross-rank execution when EP is in scope.

Use existing `golden` execution and comparison facilities. Keep operator kernels,
corresponding Torch goldens and bounded executable validation under their actual
owners. Permanent validation cannot exist only under experiment artifacts.
Verify that standalone validation calls the same compute symbols and variants as
the complete model. Record applicable CI discovery results and platform ownership;
checkpoint-specific generation is separate from default operator validation.

## Local task inputs

Provide target checkout, harness checkout, experiment directory, read-only model
root, selected environment/toolchain, requested physical devices and parallel
mapping. Derive PyPTO's dependency pins from the selected checkout. Do not treat
DP and EP group sizes on the same ranks as additional physical cards.

For serving ABI work, inspect the actual serving checkout when available; separate
model-side ABI definitions from an implemented adapter and serving execution.
The generic initial task does not implement serving.

## Host lifecycle

The launched model agent uses native goal controls exposed by its host and saves
actual status/completion results. This repository supplies no goal API bindings.
If the host lacks a capability, report the precise limitation rather than claiming
that a prompt file activated a goal. Delegation remains optional and authorized.
