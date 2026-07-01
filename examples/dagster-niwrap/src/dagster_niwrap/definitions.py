"""Dagster code location for the dagster-niwrap example."""

import dagster as dg

from dagster_niwrap.pipeline import niwrap_job

defs = dg.Definitions(jobs=[niwrap_job])
