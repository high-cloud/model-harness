# Environment record

Environment revision: draft. Keep machine-specific values in the local
experiment directory; do not commit credentials, device logs or private paths.

The owner fills this record before implementation or expensive reference and
device work. The selected integration is the source of concrete installation
commands. This file records what was inspected, installed, verified and left
unperformed; a proposed command is not execution evidence.

## Target and allocation

| Field | Value / evidence |
| --- | --- |
| Target project and revision | TBD |
| Backend integration and revision | TBD |
| Platform (`sim` or device) | TBD |
| Host architecture / OS | TBD |
| Python executable and environment | TBD |
| Physical devices allocated | TBD |
| Requested topology and rank mapping | TBD |
| Experiment directory | TBD |

## PyPTO dependency pins

Record the values from the selected PyPTO checkout, not from an old log or a
previous environment.

| Component | Source of truth | Selected value / evidence |
| --- | --- | --- |
| PyPTO checkout and commit | selected checkout | TBD |
| simpler runtime checkout and commit | PyPTO `runtime/` submodule | TBD |
| PTOAS release and architecture | PyPTO `toolchain/versions.env` and host architecture | TBD |
| PTO ISA commit | PyPTO `runtime/pto_isa.pin` | TBD |
| Target project source path | target checkout | TBD |
| `PYTHONPATH` | target project instructions | TBD |
| `PTOAS_ROOT` | selected PTOAS installation | TBD |
| CANN/toolkit revision, when using devices | selected `set_env.sh` and host inspection | TBD |

## Preparation ledger

| Step | Command or source | Status (`inspected` / `performed` / `deferred`) | Actual result / artifact |
| --- | --- | --- | --- |
| Target setup instructions read | TBD | TBD | TBD |
| Existing environment and compiler inspected | TBD | TBD | TBD |
| Python environment created or selected | TBD | TBD | TBD |
| PyPTO submodules initialized | TBD | TBD | TBD |
| CANN environment sourced, when required | TBD | TBD | TBD |
| PyPTO installed from selected checkout | TBD | TBD | TBD |
| simpler runtime installed from the selected `runtime/` | TBD | TBD | TBD |
| Pinned PTOAS installed and exported | TBD | TBD | TBD |
| Pinned PTO ISA resolved | TBD | TBD | TBD |
| Imports and dependency revisions verified | TBD | TBD | TBD |
| Integration smoke test completed | TBD | TBD | TBD |

## Verification and handoff

Record actual commands, exit codes and paths for:

- `import pypto`, `import torch`, and the target project's reference/golden
  harness;
- the pinned PTOAS executable responding to `--version`;
- the simpler revision matching the selected PyPTO `runtime/` submodule;
- the PTO ISA checkout matching `runtime/pto_isa.pin`;
- the target repository import path and required exported roots;
- the integration's smallest simulator or allocated-device smoke test.

Do not substitute a visible but unallocated device for a device smoke test.
Report network installs, CANN activation, device execution and any unresolved
toolchain step as deferred or failed. A simulator smoke test does not close a
device-environment requirement.

## Open environment findings

| Finding | Impact | Owner / remedy | Status |
| --- | --- | --- | --- |
| TBD | TBD | TBD | open |
