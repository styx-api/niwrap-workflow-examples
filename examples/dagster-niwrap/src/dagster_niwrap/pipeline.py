"""Dagster ops and job for the NiWrap neuroimaging pipeline.

The pipeline consists of two ops:

1. ``anatomical_preprocess`` — FSL BET skull-stripping followed by ANTs N4
   bias-field correction.
2. ``registration_to_template`` — ANTs registration of the preprocessed T1w
   to the MNI152NLin2009cAsym template.

They are composed into the ``niwrap_job`` job.
"""

import shutil
from pathlib import Path

import dagster as dg
import niwrap
from niwrap import ants, fsl

TEMPLATE = "MNI152NLin2009cAsym"


@dg.op
def anatomical_preprocess(
    data_dir: str,
    output_dir: str,
    subject: str,
    bet_fractional_intensity: float | None = None,
) -> Path:
    """Skull-strip and bias-field correct a subject's T1w image."""
    niwrap.use_auto()

    t1w_path = (
        Path(data_dir).resolve()
        / "ds000001"
        / f"sub-{subject}"
        / "anat"
        / f"sub-{subject}_T1w.nii.gz"
    )
    if not t1w_path.exists():
        raise FileNotFoundError(f"T1w image not found: {t1w_path}")
    output = (
        Path(output_dir).resolve()
        / "preprocess"
        / f"sub-{subject}_desc-preproc_T1w.nii.gz"
    )
    output.parent.mkdir(parents=True, exist_ok=True)

    bet = fsl.bet(infile=t1w_path, fractional_intensity=bet_fractional_intensity)
    n4 = ants.n4_bias_field_correction(
        input_image=bet.outfile,
        image_dimensionality=3,
        output=ants.n4_bias_field_correction_corrected_output_params(
            corrected_output_file_name=output.name
        ),
    )

    shutil.copy2(str(n4.output_image_outfile), output)
    return output


@dg.op
def registration_to_template(
    preproc_t1w: Path,
    output_dir: str,
    data_dir: str,
    subject: str,
) -> None:
    """Register the preprocessed T1w image to the template space."""
    niwrap.use_auto()

    output = (
        Path(output_dir).resolve()
        / "registration"
        / f"sub-{subject}_space-{TEMPLATE}_desc-preproc_T1w.nii.gz"
    )
    output.parent.mkdir(parents=True, exist_ok=True)

    template_t1w = (
        Path(data_dir).resolve()
        / "templateflow"
        / f"tpl-{TEMPLATE}"
        / f"tpl-{TEMPLATE}_res-01_T1w.nii.gz"
    )
    prefix = "t1w_to_template_"
    xfm = ants.ants_registration_sy_n_quick_sh(
        dimensionality=3,
        fixed_image=template_t1w,
        moving_image=Path(preproc_t1w).resolve(),
        output_prefix=prefix,
    )

    shutil.copy2(str(xfm.root / f"{prefix}Warped.nii.gz"), output)


@dg.job
def niwrap_job() -> None:
    """Run the full BET → N4 → registration pipeline."""
    registration_to_template(anatomical_preprocess())
