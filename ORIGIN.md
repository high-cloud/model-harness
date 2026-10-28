# Provenance

The initial prompts and seven templates were extracted and adapted from
[high-cloud/pypto-lib, commit bede719179dc844d154830defa5084a06bc83cd5](https://github.com/high-cloud/pypto-lib/tree/bede719179dc844d154830defa5084a06bc83cd5/docs/model-development).
The common model rules were adapted from `.claude/rules/models.md` at that same
commit, including the PyPTO-Lib contributors' model-organization guidance.

The extraction replaces repository-relative references with standalone rules and
integration documentation, and separates target-specific execution details from
the common workflow. The PyPTO environment guide is adapted from the target
project's setup skill and installation guide; the selected target checkout
remains authoritative for changing commands and pins. Model implementations and
experiment artifacts were not copied.
