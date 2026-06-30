# NiWrap Workflow Examples

Examples of using [NiWrap](https://github.com/childmindresearch/niwrap) with different workflow engines.

Each example implements the same minimal neuroimaging pipeline:

1. **BET** — skull-strip the T1w image with FSL.
2. **N4 bias-field correction** — correct intensity inhomogeneity with ANTs.
3. **Template registration** — register the preprocessed T1w to MNI152NLin2009cAsym with ANTs.

These are intentionally simple examples that demonstrate chaining two steps
(preprocessing and registration) with NiWrap and different workflow enngines.
They are starting points for building more complex workflows.

## Running an example

Run from the repository root:

| Engine | Command |
| --- | --- |
| snakemake | `uv run snakemake --snakefile examples/snakemake-niwrap/src/snakemake_niwrap/Snakefile --cores 1` |

## Examples

| Workflow engine | Description |
| --- | --- |
| [`dagster`](examples/dagster-niwrap) | Orchestration platform ([website](https://dagster.io/)) |
| [`nextflow`](examples/nextflow-niwrap) | DSL for data-driven computational pipelines ([website](https://github.com/nextflow-io/nextflow)) |
| [`snakemake`](examples/snakemake-niwrap) | Workflow management tool to create reproducible and scalable data analysis ([website](https://snakemake.github.io/)) |

## Development

This is a [uv workspace](https://docs.astral.sh/uv/concepts/projects/workspaces/).
All tooling and CI runs against the whole workspace.

```bash
# Install every workspace member into a shared venv.
uv sync --all-packages

# Lint and format.
uv run ruff check
uv run ruff format --check
uv run ty examples/
```
