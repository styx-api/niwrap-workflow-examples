"""Dagster assets for the NiWrap neuroimaging pipeline.

The pipeline consists of two assets:

1. ``anatomical_preprocess`` — FSL BET skull-stripping followed by ANTs N4
   bias-field correction.
2. ``registered_t1w`` — ANTs registration of the preprocessed T1w to the
   MNI152NLin2009cAsym template.
"""

import shutil
from pathlib import Path

import dagster as dg
import niwrap
from niwrap import ants, fsl

TEMPLATE = "MNI152NLin2009cAsym"


class DagsterNiftiConfig(dg.Config):
    """Shared configuration for the NiWrap pipeline assets."""

    data_dir: str
    output_dir: str
    subject: str
    bet_fractional_intensity: float | None = None


@dg.asset
def anatomical_preprocess(config: DagsterNiftiConfig) -> str:
    """Skull-strip and bias-field correct a subject's T1w image."""
    niwrap.use_auto()

    t1w_path = (
        Path(config.data_dir).resolve()
        / "ds000001"
        / f"sub-{config.subject}"
        / "anat"
        / f"sub-{config.subject}_T1w.nii.gz"
    )
    if not t1w_path.exists():
        raise FileNotFoundError(f"T1w image not found: {t1w_path}")
    output = (
        Path(config.output_dir).resolve()
        / "preprocess"
        / f"sub-{config.subject}_desc-preproc_T1w.nii.gz"
    )
    output.parent.mkdir(parents=True, exist_ok=True)

    bet = fsl.bet(infile=t1w_path, fractional_intensity=config.bet_fractional_intensity)
    n4 = ants.n4_bias_field_correction(
        input_image=bet.outfile,
        image_dimensionality=3,
        output=ants.n4_bias_field_correction_corrected_output_params(
            corrected_output_file_name=output.name
        ),
    )
    if n4.output_image_outfile is None:
        raise FileNotFoundError("Bias-field corrected output not found.")

    shutil.copy2(n4.output_image_outfile, output)
    return str(output)


@dg.asset
def registered_t1w(config: DagsterNiftiConfig, anatomical_preprocess: str) -> None:
    """Register the preprocessed T1w image to the template space."""
    niwrap.use_auto()

    output = (
        Path(config.output_dir).resolve()
        / "registration"
        / f"sub-{config.subject}_space-{TEMPLATE}_desc-preproc_T1w.nii.gz"
    )
    output.parent.mkdir(parents=True, exist_ok=True)

    template_t1w = (
        Path(config.data_dir).resolve()
        / "templateflow"
        / f"tpl-{TEMPLATE}"
        / f"tpl-{TEMPLATE}_res-01_T1w.nii.gz"
    )
    prefix = "t1w_to_template_"
    xfm = ants.ants_registration_sy_n_quick_sh(
        dimensionality=3,
        fixed_image=template_t1w,
        moving_image=Path(anatomical_preprocess).resolve(),
        output_prefix=prefix,
    )

    shutil.copy2(xfm.root / f"{prefix}Warped.nii.gz", output)
