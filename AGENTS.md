# Model Harness Agent Instructions

Read README.md, rules/models.md and the relevant project integration before
changing prompts or templates. Keep the workflow lightweight: native goals,
existing project tools and Markdown evidence, without another scheduler.

- Preserve model-owner responsibility for implementation, verification and goal
  closeout. Do not add a mandatory parent-agent approval step.
- Keep common constraints in rules/ and target-project APIs in integrations/.
- Keep prompts and all affected templates aligned when requirements change.
- Distinguish documented requirements from implemented checks and executed results.
- Keep checkpoints, model implementations, machine paths and execution logs out
  of this repository. Write maintained documentation in English.
- Run tools/check_docs.py and the tests after changes. Run all pre-commit hooks
  before committing. Use Type: imperative commit subjects and describe only the
  actual change. Do not bypass hooks or add AI co-author credits.
