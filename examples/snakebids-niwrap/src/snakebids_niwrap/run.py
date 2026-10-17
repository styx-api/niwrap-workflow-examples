"""Entry point for the snakebids-niwrap example application."""

import argparse
from pathlib import Path

from snakebids import bidsapp, plugins

app = bidsapp.app([plugins.SnakemakeBidsApp(Path(__file__).parent)])


def get_parser() -> argparse.ArgumentParser:
    """Expose the parser (e.g. for Sphinx argparse docs)."""
    return app.build_parser().parser


def main() -> None:
    """Run the snakebids app from this package directory."""
    app.run()


if __name__ == "__main__":
    main()
