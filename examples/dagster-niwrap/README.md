# dagster-niwrap

A minimal example of using [NiWrap](https://github.com/childmindresearch/niwrap) with [Dagster](https://dagster.io/).

## Setup

This example is a member of the root [uv workspace](../../pyproject.toml). From the repository root:

```bash
uv sync --all-packages
```

## Run

### Headless

From the repository root:

```bash
uv run dagster job execute -m dagster_niwrap -j niwrap_job --config examples/dagster-niwrap/config.json
```

### Interactive UI

From the repository root:

```bash
uv run dagster dev -m dagster_niwrap
```

Then open http://localhost:3000 in your browser and launch the `niwrap_job` job.

## Configuration

Create a `config.json` file with the run config:

```json
{
  "ops": {
    "anatomical_preprocess": {
      "inputs": {
        "data_dir": "examples/.data",
        "output_dir": "examples/dagster-niwrap/output",
        "subject": "01",
        "bet_fractional_intensity": 0.5
      }
    },
    "registration_to_template": {
      "inputs": {
        "output_dir": "examples/dagster-niwrap/output",
        "data_dir": "examples/.data",
        "subject": "01"
      }
    }
  }
}
```

Paths in the config are relative to the repository root because the run command is invoked from the repository root. Adjust them as needed. If `bet_fractional_intensity` is omitted, it defaults to `None`.

## Dependencies

- `dagster>=1.9.0`
- `dagster-webserver>=1.9.0`
- `niwrap>=1.0.4`

See [`pyproject.toml`](pyproject.toml) for details.

## Linting and formatting

The Python files are linted and formatted with `ruff`:

```bash
uv run ruff check src/dagster_niwrap/
uv run ruff format --check src/dagster_niwrap/
uv run ty check src/dagster_niwrap/
```
