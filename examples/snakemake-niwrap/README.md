# snakemake-niwrap

A minimal example of using [NiWrap](https://github.com/childmindresearch/niwrap) with [Snakemake](https://snakemake.github.io/).

## Setup

This example is a member of the root [uv workspace](../../pyproject.toml). From the repository root:

```bash
uv sync --all-packages
```

## Run

Change into the directory containing the `Snakefile`:

```bash
cd examples/snakemake-niwrap/src/snakemake_niwrap
uv run snakemake --cores 1
```

## Configuration

Edit [`config.yaml`](src/snakemake_niwrap/config.yaml) before running:

- `data_dir`: directory containing the input dataset.
- `output_dir`: directory where results are written.
- `subject`: list of subject labels to process.
- `bet_fractional_intensity`: fractional intensity threshold for FSL BET.

Paths are relative to the workflow directory (where the `Snakefile` is located)
unless an absolute path is provided.

## Dependencies

- `niwrap>=1.0.4`
- `snakemake>=9.23.1`

See [`pyproject.toml`](pyproject.toml) for details.

## Linting and formatting

The `Snakefile` is formatted with [`snakefmt`](https://github.com/snakemake/snakefmt):

```bash
uv tool run snakefmt src/snakemake_niwrap/Snakefile
```

`ruff` does not lint Snakemake files; this example contains no other Python files.
