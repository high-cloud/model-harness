# Regression cases for project integrations

These are acceptance scenarios for checks implemented in the target project.
They do not claim a generic static checker can prove model behavior.

| Scenario | Required observation |
| --- | --- |
| Prompt-token loop encloses the whole decoder stack | Reject default multi-token prefill, even if compiled and numerically correct |
| Identical wrappers are renamed prefill and decode | Inspect expanded loops and logical token shapes; names cannot establish phase behavior |
| Rows are padded, or represent heads/routes from one token | Do not count them as multiple logical prompt tokens |
| Necessary recurrent scan within a layer | Allow it when multi-token projections and feed-forward structure satisfy the contract |
| Expert fixture sends multiple tokens to one expert | Demonstrate supported grouping and correct weighted combine without dropping routes |
| Standalone validation calls an earlier numerical variant | Keep delivered variant unaccepted until its actual path is verified |
| Only an experiment-local script implements required validation | Keep engineering acceptance open until permanent validation is in target sources |
| Generation is coherent but engineering requirements are unresolved | Keep required rows and the implementation goal incomplete |
| Source or compiled evidence is missing or unrecognized | Do not convert unknown evidence into a pass |

For executable structural controls, run the actual compiled path and a deliberate
tokenwise full-stack substitute through the same check. Record commands, source
and build identities, evidence locations and actual rejection. Repeat the negative
control with renamed wrappers. Keep model-specific inspection beside the owning
validation entry and reuse the project's existing tools.
