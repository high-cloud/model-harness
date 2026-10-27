# Model Harness

Prompts, contracts and acceptance templates for agents implementing inference
models. The model agent owns implementation, validation, repair and completion.
Use the host's native goal facility when available, with Markdown checklists;
this repository does not provide a workflow engine or an agent runtime.

The initial release provides reusable documents and a PyPTO integration guide.
It does not include an automatic model-acceptance engine. Structural and numerical
checks must execute against the actual model sources and compiled artifacts in
the target project. A completed checklist alone is not execution evidence.

## Start a model task

1. Read the target project's agent instructions and [model rules](rules/models.md).
2. Select the project integration; [PyPTO](integrations/pypto/README.md) is the
   first supported integration guide.
3. Copy all six [templates](#templates) into a local experiment directory in the
   target project. Supply checkpoint, project, environment and artifact paths in
   local inputs; keep checkpoints read-only.
4. Give the launched agent the [main prompt](prompts/PROMPT.md), the absolute
   location of this harness checkout, the selected integration and the experiment
   directory. Resolve relative links in prompts against this checkout, even if
   prompt text is pasted into another host. Use the
   [worker prompt](prompts/WORKER_PROMPT.md) only when delegation is authorized.
5. Agree the model scope, topology, interfaces and acceptance, then activate the
   implementation goal using the host's actual controls. The model agent executes
   acceptance and closes the goal itself; parent review is not a completion gate.

When copying templates, replace links to `../rules/models.md` with the location
of this checkout or a commit permalink. Template filenames and draft markers
are intentional; fill them before accepting an implementation. See the
[launch input example](examples/launch-inputs.md).

## Required checkpoints

- Before implementation, map operator ownership, goldens, default validation,
  comparators and actual composition consumers.
- On the first working attention and MoE/feed-forward paths, inspect dependencies,
  call depth, phase shapes and validation-to-composition symbol identity before
  scaling the full model. Repeat for distinct hybrid mixers.
- Before completion, verify multi-token prefill structure, numerical/state gates,
  checkpoint mapping, real-device generation, default validation and applicable
  CI discovery. Execute a negative control that must reject tokenwise full-stack
  prefill. See [acceptance criteria](templates/ACCEPTANCE.md).

Necessary recurrent scans and tiled scheduling are allowed. A prompt-token loop
through the whole decoder stack is diagnostic-only by default, even inside
compiled orchestration. Excluding performance tuning does not waive structure.
Full-model exact token parity, semantic generation, serving execution and
performance acceptance are separate claims. The default scope ends at real-weight
model generation and defines a future serving ABI; serving execution requires
an explicit scope extension and additional checks.

## Templates

| File | Purpose |
| --- | --- |
| [MODEL_SPEC.md](templates/MODEL_SPEC.md) | Model facts, scope, topology and execution contract |
| [MODULES.md](templates/MODULES.md) | Ownership, tensor contracts, consumers and first-path checks |
| [ACCEPTANCE.md](templates/ACCEPTANCE.md) | Engineering, structural, numerical and generation gates |
| [WEIGHT_MANIFEST.md](templates/WEIGHT_MANIFEST.md) | Checkpoint conversion and complete destination mapping |
| [SERVING_ABI.md](templates/SERVING_ABI.md) | Future serving call and persistent-state contract |
| [TASKS.md](templates/TASKS.md) | Execution evidence, open findings and goal closeout |

## Repository boundaries

Common agent constraints live in `rules/`; project-specific setup, DSL style,
comparison APIs, compiler inspection and device queues are referenced through
`integrations/`. Target project rules remain authoritative for their concrete
APIs. Resolve genuine conflicts explicitly instead of silently waiving a gate.

Model code, operator goldens, permanent model validation and model-specific
structural checks stay in the target project. Weights, compiled builds, device
logs and task-specific filled templates stay in local experiment storage.
This repository contains generic documents and small reproducible examples.

## Development

```bash
python3 tools/check_docs.py
python3 -m unittest discover -s tests -v
pre-commit run --all-files
```

These commands validate this repository's documentation and its checker. They
do not validate any model's numerical results or execution structure. The
[regression cases](examples/regression-cases.md) describe required target-project
negative controls; they are not already implemented model acceptance tests.

See [provenance](ORIGIN.md) for the extraction source.
