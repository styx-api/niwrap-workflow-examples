"""Run FSL BET and ANTs N4 bias-field correction on a T1w image."""

import argparse
import shutil
from pathlib import Path

import niwrap
from niwrap import ants, fsl


def _existing_path(value: str) -> Path:
    """Return a Path only if it exists."""
    path = Path(value)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"Path does not exist: {path}")
    return path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Skull-strip and bias-field correct a T1w image."
    )
    parser.add_argument(
        "--t1w",
        type=_existing_path,
        required=True,
        help="Path to the input T1w NIfTI image.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path where the corrected output image is written.",
    )
    parser.add_argument(
        "--bet-fractional-intensity",
        type=float,
        default=None,
        help="Optional fractional intensity parameter for FSL BET.",
    )
    return parser.parse_args()


def main() -> None:
    """Run BET and N4 on the input T1w image."""
    args = parse_args()

    niwrap.use_auto()

    bet = fsl.bet(infile=args.t1w, fractional_intensity=args.bet_fractional_intensity)
    n4 = ants.n4_bias_field_correction(
        input_image=bet.outfile,
        image_dimensionality=3,
        output=ants.n4_bias_field_correction_corrected_output_params(
            corrected_output_file_name=args.output.name
        ),
    )

    if n4.output_image_outfile is None:
        raise FileNotFoundError("Bias corrected image not found.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(n4.output_image_outfile, args.output)


if __name__ == "__main__":
    main()
