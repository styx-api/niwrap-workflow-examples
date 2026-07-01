"""Dagster-NiWrap example package.

This package contains a Dagster job that runs a neuroimaging pipeline built with
NiWrap. The entry points are exported from ``definitions.py``.
"""

from dagster_niwrap.definitions import defs

__all__ = ["defs"]
