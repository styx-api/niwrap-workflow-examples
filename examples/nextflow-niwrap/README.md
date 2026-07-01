# nextflow-niwrap

A minimal example of using [NiWrap](https://github.com/childmindresearch/niwrap) with [Nextflow](https://www.nextflow.io/).

## Setup

1. Install Nextflow if you have not already:

   ```bash
   curl -s https://get.nextflow.io | bash
   ```

   Or use your package manager (e.g., `brew install nextflow`).

2. From the repository root, install the Python workspace:

   ```bash
   uv sync --all-packages
   ```

## Run

From this directory:

```bash
nextflow run main.nf
```

Or with custom parameters:

```bash
nextflow run main.nf \
    --data_dir /path/to/data \
    --output_dir /path/to/output \
    --subject 01 \
    --bet_fractional_intensity 0.5
```

## Python environment

The helper scripts in `src/nextflow_niwrap/` use NiWrap, so the Python
environment that Nextflow sees must have `niwrap`, `niwrap-fsl`, and
`niwrap-ants` installed.

By default, `nextflow.config` sets:

```groovy
params.python_cmd = "uv run python3"
```

This lets Nextflow call Python through the workspace venv without you having
to activate it manually. If you prefer to use a different environment
(conda, virtualenv, etc.), edit `params.python_cmd` or activate the
environment before running Nextflow.

## Configuration

Edit [`nextflow.config`](nextflow.config) or pass parameters on the command
line:

- `data_dir`: directory containing `ds000001/` and `templateflow/`.
- `output_dir`: directory where `preprocess/` and `registration/` results are written.
- `subject`: subject label to process (e.g., `01`).
- `template`: template name (default: `MNI152NLin2009cAsym`).
- `bet_fractional_intensity`: fractional intensity threshold for FSL BET.

## Dependencies

- Nextflow
- Python packages installed by the root workspace:
  - `niwrap`

See the root [`pyproject.toml`](../../pyproject.toml) for the full dependency list.

## Linting and formatting

The helper scripts are plain Python and can be linted with `ruff`:

```bash
uv run ruff check src/nextflow_niwrap/
uv run ruff format --check src/nextflow_niwrap/
```
