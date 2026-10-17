# snakebids-niwrap

A minimal example of using [NiWrap](https://github.com/childmindresearch/niwrap) with [Snakebids](https://snakebids.readthedocs.io/).

## Setup

This example is a member of the root [uv workspace](../../pyproject.toml). From the repository root:

```bash
uv sync --all-packages
```

## Run

The example installs a `snakebids-niwrap` console script. From the repository root:

```bash
uv run snakebids-niwrap /path/to/bids /path/to/output participant --cores 1
```

Or, after installing the package, run directly:

```bash
snakebids-niwrap /path/to/bids /path/to/output participant --cores 1
```

## Configuration

Edit [`src/snakebids_niwrap/config/snakebids.yaml`](src/snakebids_niwrap/config/snakebids.yaml) to set defaults for:

- `bids_dir`: path to the input BIDS dataset.
- `output_dir`: path where results are written.
- `pybids_inputs`: inputs discovered by PyBIDS.
- `parse_args`: additional CLI arguments (e.g., `--bet_fractional_intensity`).

The workflow expects a `templateflow/` directory as a sibling of `bids_dir` with
a `tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_res-01_T1w.nii.gz` template
file for registration.

## Dependencies

- `niwrap>=1.0.4`
- `snakebids>=0.15.0`

See [`pyproject.toml`](pyproject.toml) for details.

## Linting and formatting

The `Snakefile` is formatted with [`snakefmt`](https://github.com/snakemake/snakefmt):

```bash
uv tool run snakefmt src/snakebids_niwrap/workflow/Snakefile
```

Python files are linted and formatted with `ruff`:

```bash
uv run ruff check src/snakebids_niwrap/
uv run ruff format --check src/snakebids_niwrap/
```
