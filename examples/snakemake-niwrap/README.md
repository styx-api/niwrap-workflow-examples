# snakemake-niwrap

A minimal example of using [NiWrap](https://github.com/childmindresearch/niwrap) with [Snakemake](https://snakemake.github.io/).

## Setup

This example is a member of the root [uv workspace](../../pyproject.toml). From the repository root:

```bash
uv sync --all-packages
```

## Run

From the repository root:

```bash
uv run snakemake -s examples/snakemake-niwrap/src/snakemake_niwrap/Snakefile --cores 1
```

> **Windows users:** Snakemake's metadata filenames can exceed the 260-character
> `MAX_PATH` limit for deep output directories. Use a short `output_dir` (e.g.
> `C:\out`), enable Windows long paths (`core.longpaths`), or run under WSL.

## Configuration

Edit [`config.yaml`](src/snakemake_niwrap/config.yaml) before running:

- `data_dir`: directory containing the input dataset.
- `output_dir`: directory where results are written.
- `subject`: list of subject labels to process.
- `bet_fractional_intensity`: fractional intensity threshold for FSL BET.

Relative paths are resolved from the directory you invoke `snakemake` from
(the repository root, per the command above). Absolute paths may also be provided.

## Dependencies

- `niwrap>=1.0.4`
- `snakemake>=9.23.1`

See [`pyproject.toml`](pyproject.toml) for details.

## Linting and formatting

The `Snakefile` is formatted with [`snakefmt`](https://github.com/snakemake/snakefmt):

```bash
uv tool run snakefmt src/snakemake_niwrap/Snakefile
```

Python scripts under [`scripts/`](src/snakemake_niwrap/scripts) are linted and
formatted with `ruff` from the workspace root:

```bash
uv run ruff check
uv run ruff format --check
```
