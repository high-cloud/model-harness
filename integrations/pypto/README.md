# PyPTO integration

Use Model Harness alongside a target checkout of
[pypto-lib](https://github.com/hw-native-sys/pypto-lib). This guide maps generic
requirements to the project's owning files; it does not duplicate its DSL style
or provide its runtime, device queue or goal host. Record the result in the
[environment template](../../templates/ENVIRONMENT.md) before implementation.

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

## Prepare and verify the environment

Use the target checkout's setup skill and installation guide as the executable
source. Keep the following order and record each step's actual result:

1. Inspect the requested simulator or device platform, host architecture,
   Python environment, compilers, existing PyPTO/PTOAS checkouts and exported
   roots. For a device run, verify an allocated device and inspect CANN with
   `npu-smi info`.
2. Reuse the selected PyPTO checkout or create a separate checkout without
   overwriting an existing one. Initialize its submodules and derive the
   PTOAS release from that checkout's `toolchain/versions.env`.
3. For a device target, source the selected CANN `set_env.sh` before installing
   PyPTO's `runtime/` submodule. This lets the simpler build find the required
   device compilers; sourcing CANN afterwards does not repair an already-built
   runtime.
4. Install PyPTO from the selected checkout and simpler from that checkout's
   `runtime/`. Install the pinned PTOAS release under `PTOAS_ROOT`; do not
   copy versions from an earlier run. Let simpler resolve the PTO ISA revision
   from `runtime/pto_isa.pin`.
5. Verify `pypto`, `torch` and the target golden/reference imports; probe the
   pinned PTOAS executable with `--version`; verify the simpler and PTO ISA
   revisions; and confirm `PYTHONPATH` and required roots in the shell that
   will run the case.
6. Run the integration's smallest `hello_world`-style simulator smoke test or
   an allocated-device smoke test. A simulator pass does not close a device
   requirement. Report network installation, CANN activation, device
   execution, or PTO ISA resolution as deferred when they were not performed.

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
