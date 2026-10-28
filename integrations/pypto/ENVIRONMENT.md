# PyPTO environment preparation

This guide prepares a target `pypto-lib` checkout for simulator or Ascend
device work. It is adapted from the target project's `setup-env` skill and
installation guide. Read those files in the selected checkout first: their
commands and toolchain requirements are authoritative when they differ from
this guide. Record actual commands, revisions, exit codes and deferred steps
in the [environment record](../../templates/ENVIRONMENT.md).

The workflow keeps PyPTO, simpler, PTOAS and PTO ISA aligned to one selected
PyPTO checkout. It does not install drivers or firmware, allocate devices, or
submit jobs to a queue on the user's behalf.

## 1. Inspect before changing anything

Choose the execution target explicitly. Do not infer a simulator or device
platform from host architecture; architecture only selects the PTOAS asset,
while the `-p` option selects the platform.

Record the following before installing or mutating an environment:

```bash
uname -a
python3 --version
git --version
cmake --version
ninja --version
which python3
which gcc || true
which g++ || true
printf 'PYTHONPATH=%s\nPTOAS_ROOT=%s\nPTO_ISA_ROOT=%s\n' \
  "${PYTHONPATH-}" "${PTOAS_ROOT-}" "${PTO_ISA_ROOT-}"
```

Also record the target project's revision, existing PyPTO/PTOAS/PTO ISA
checkouts, requested platform, allocated physical devices and parallel group
mapping. For a device target, `npu-smi info` must show an allocated device:

```bash
npu-smi info
```

Use only devices allocated to the task. A visible device without an allocation
does not authorize a device run.

## 2. Create or select the Python environment

Run these commands from the target `pypto-lib` checkout. Reuse a user-selected
environment when required by the target project; otherwise a local virtual
environment keeps the install isolated:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install scikit-build-core nanobind cmake ninja
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu

export PYPTO_LIB_ROOT="$PWD"
export PYTHONPATH="$PYPTO_LIB_ROOT${PYTHONPATH:+:$PYTHONPATH}"
```

Install the CPU Torch wheel before PyPTO. This avoids resolving the generic
Torch requirement to an unused CUDA stack. Simulator builds require a C++17
compiler and the target's simulator compiler requirement; the current
`pypto-lib` installation guide requires `gcc-15` and `g++-15` for simulator
platforms. Use the selected checkout's guide if that requirement changes.

## 3. Prepare CANN for device work

Skip this section for simulator-only work. Driver and firmware are host-level
dependencies and normally require an administrator; do not install or modify
them as part of an agent task. Verify the driver first:

```bash
npu-smi info
```

Source the selected user-accessible CANN toolkit before installing the PyPTO
runtime. The toolkit path is site-specific:

```bash
export CANN_ROOT=<selected-cann-toolkit-root>
source "$CANN_ROOT/set_env.sh"
test -n "${ASCEND_HOME_PATH-}"
test -x "$ASCEND_HOME_PATH/bin/ccec"
test -f "$ASCEND_HOME_PATH/tools/hcc/bin/aarch64-target-linux-gnu-g++"
```

The simpler runtime detects these compilers while it is installed. Sourcing
CANN after installing `runtime/` does not rebuild an onboard runtime that was
compiled without the device toolchain; source CANN and reinstall `runtime/`
if that happened. Keep CANN package installation and any administrator action
visible as deferred when they were not performed.

## 4. Select and pin the PyPTO checkout

Reuse a selected checkout when one exists. Otherwise clone into a scoped
sibling directory without overwriting another checkout:

```bash
git clone --recurse-submodules https://github.com/hw-native-sys/pypto.git <pypto-root>
export PYPTO_ROOT="$(cd <pypto-root> && pwd)"
git -C "$PYPTO_ROOT" submodule update --init --recursive
```

Do not replace `<pypto-root>` with a private machine path in maintained
documentation. Record the selected PyPTO commit and the submodule status in
the local environment record.

Derive every dependency from this checkout:

```bash
export PTOAS_VERSION="$(sed -n 's/^PTOAS_VERSION=//p' \
  "$PYPTO_ROOT/toolchain/versions.env")"
export PTO_ISA_PIN="$(cat "$PYPTO_ROOT/runtime/pto_isa.pin")"
printf 'PyPTO=%s\nPTOAS=%s\nPTO-ISA=%s\n' \
  "$(git -C "$PYPTO_ROOT" rev-parse HEAD)" "$PTOAS_VERSION" "$PTO_ISA_PIN"
```

Never copy a PTOAS version or PTO ISA commit from an earlier log.

## 5. Install PyPTO and simpler

Install both packages from the selected checkout, without build isolation so
the active environment and compiler selection are used:

```bash
python -m pip install --no-build-isolation "$PYPTO_ROOT"
python -m pip install --no-build-isolation "$PYPTO_ROOT/runtime"
```

The `runtime/` directory is the simpler submodule pinned by this PyPTO
revision. Installing another runtime checkout breaks the intended pin. On a
device target, the CANN environment from step 3 must be active before the
second command. Confirm that the requested simulator or device binaries were
built by the installer.

## 6. Install the pinned PTOAS release

Use the architecture reported by `uname -m` and the version read from the
selected PyPTO checkout. The release bundle is kept outside the source tree:

```bash
export PTOAS_ARCH="$(uname -m)"
curl -fL -O \
  "https://github.com/hw-native-sys/PTOAS/releases/download/$PTOAS_VERSION/ptoas-bin-$PTOAS_ARCH.tar.gz"
mkdir -p ../ptoas-bin
tar -xzf "ptoas-bin-$PTOAS_ARCH.tar.gz" -C ../ptoas-bin
export PTOAS_ROOT="$(cd ../ptoas-bin && pwd)"
```

Use the asset naming and installation method in the selected target guide if
that release uses a wheel or a different bundle. The `PTOAS_ROOT` directory
must be the only PTOAS installation searched by the run shell.

## 7. Resolve the pinned PTO ISA

Do not clone PTO ISA manually or use `PTO_ISA_ROOT` to substitute another
revision. simpler owns one managed checkout and uses `runtime/pto_isa.pin`.
The first use may clone it and can pause on a slow or blocked network.

After PyPTO and simpler are installed, resolve the managed checkout and verify
its commit:

```bash
export PTO_ISA_ROOT="$(python -c \
  'import pypto.runtime; print(pypto.runtime.ensure_pto_isa_root())')"
test "$(git -C "$PTO_ISA_ROOT" rev-parse HEAD)" = "$PTO_ISA_PIN"
```

If the checkout is dirty or at another revision, let simpler recreate it or
repair it through the target project's documented workflow. Do not silently
continue with a mismatched tree.

## 8. Verify the complete shell

Run verification in the same activated shell that will compile or execute the
model:

```bash
python -c "import pypto, torch; from golden import run; print(pypto.__file__); print(torch.__version__)"

PTOAS_BIN=
for candidate in "$PTOAS_ROOT/ptoas" "$PTOAS_ROOT/ptoas.sh" "$PTOAS_ROOT/bin/ptoas"; do
  if test -x "$candidate"; then PTOAS_BIN="$candidate"; break; fi
done
test -n "$PTOAS_BIN"
"$PTOAS_BIN" --version

git -C "$PYPTO_ROOT/runtime" rev-parse HEAD
printf 'PTOAS_ROOT=%s\nPTO_ISA_ROOT=%s\nPYTHONPATH=%s\n' \
  "$PTOAS_ROOT" "$PTO_ISA_ROOT" "$PYTHONPATH"
```

The PTOAS probe order matches PyPTO's locator. Verify that the printed
`runtime/` revision belongs to the selected PyPTO checkout and that the PTO
ISA commit check passed. If `pypto` resolves from an unexpected CANN site
package, fix `PYTHONPATH` ordering and reinstall the selected checkout before
continuing.

## 9. Run the smallest smoke test

For simulator work, use the target platform explicitly:

```bash
python examples/beginner/hello_world.py -p <platform> --sim
```

For device work, keep CANN sourced and use the target's allocated-device queue
workflow, such as the installed `task-submit` integration. Do not run a direct
device command when the target project requires queue submission:

```bash
<target-project-device-submit> python examples/beginner/hello_world.py \
  -p <platform> -d <allocated-device>
```

The smoke test must exercise the front end, PTOAS, runtime and selected
platform. A simulator pass does not close a device requirement. Record the
command, exit code, platform, device allocation and `[RUN] PASS` result.

## Troubleshooting

| Symptom | Likely check |
| --- | --- |
| `ModuleNotFoundError: golden` | Run from the target repository root and export that root in `PYTHONPATH`. |
| `ModuleNotFoundError: pypto` | Activate the intended environment and reinstall the selected PyPTO checkout. |
| `pypto` resolves from a CANN site package | Inspect `pypto.__file__`, then put the selected environment's site packages first in `PYTHONPATH`. |
| PTOAS cannot be found | Export `PTOAS_ROOT` and verify `ptoas`, `ptoas.sh` or `bin/ptoas` in that order. |
| First device build appears stuck | It may be cloning the pinned PTO ISA; inspect the checkout named by the resolver before interrupting it. |
| Simulator cannot find the required GCC | Verify the target guide's compiler requirement and the active `gcc`/`g++` paths. |
| Device platform is rejected while simulator works | Source CANN before installing `runtime/`, verify `ccec` and the AICPU compiler, then reinstall `runtime/`. |

## Report the result

Report the selected platform, Python environment, PyPTO commit, simpler
revision, PTOAS version and architecture, PTO ISA commit, exported roots,
allocated devices and smoke-test result. Label network installs, CANN
activation, device execution and unresolved PTO ISA resolution as inspected,
performed, deferred or failed. Only performed checks with actual evidence close
the environment-preparation row in `ENVIRONMENT.md`.
