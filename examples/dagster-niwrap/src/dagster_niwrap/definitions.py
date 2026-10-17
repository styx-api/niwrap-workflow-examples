"""Dagster code location for the dagster-niwrap example."""

import dagster as dg

from dagster_niwrap.pipeline import anatomical_preprocess, registered_t1w

defs = dg.Definitions(assets=[anatomical_preprocess, registered_t1w])
