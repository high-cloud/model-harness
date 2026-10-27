# Launch input example

Supply the following information to the model agent along with
[the main prompt](../prompts/PROMPT.md). Replace placeholders locally; do not
commit machine-specific input files.

```text
HARNESS_ROOT=<local model-harness checkout>
PROJECT_ROOT=<target model repository>
INTEGRATION=integrations/pypto/README.md
EXPERIMENT_DIR=<local experiment directory containing six copied templates>
MODEL_ROOT=<read-only checkpoint directory>
MODEL_ID=<checkpoint identity and revision>
ENVIRONMENT=<selected project environment>
REQUESTED_TOPOLOGY=<physical cards and attention/expert/tensor groups>
INITIAL_SCOPE=<dtype policy, shapes, model modes and exclusions>
```

The agent proposes the concrete specification and acceptance before kernel work,
reusing decisions already authorized by the user. Record the requested objective
and agreed decisions in the experiment's `goal.md`, which the main prompt reads.
File ownership and early-path
checks belong in MODULES.md. A two-card attention-DP2/expert-EP2 topology may use
the same two physical ranks; record group membership and request/state ownership.

The owner then implements, verifies and repairs every required row. It reports
numerical, structural and generation acceptance separately and saves actual native
goal completion only after all required rows pass on the delivered source.
