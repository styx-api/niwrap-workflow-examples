"""Entry point for the snakebids-niwrap example application.

This script builds a SnakeBidsApp from the package directory and delegates
execution to Snakemake.
"""

from argparse import ArgumentParser
from pathlib import Path

from snakebids.app import SnakeBidsApp
from snakebids.cli import add_dynamic_args


def get_parser() -> ArgumentParser:
    """Exposes parser for sphinx doc generation, working directory is the docs dir."""
    app = SnakeBidsApp(".", skip_parse_args=True)
    add_dynamic_args(app.parser, app.config["parse_args"], app.config["pybids_inputs"])
    return app.parser


def main() -> None:
    """Run the SnakeBids app from this package directory."""
    app = SnakeBidsApp(Path(__file__).parent.absolute())
    app.run_snakemake()


if __name__ == "__main__":
    main()
