"""Register a preprocessed T1w image to a template using ANTs."""

import argparse
import shutil
from pathlib import Path

import niwrap
from niwrap import ants


def _existing_path(value: str) -> Path:
    """Return a Path only if it exists."""
    path = Path(value)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"Path does not exist: {path}")
    return path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Register a preprocessed T1w image to a template."
    )
    parser.add_argument(
        "--moving",
        type=_existing_path,
        required=True,
        help="Path to the moving (preprocessed) T1w image.",
    )
    parser.add_argument(
        "--fixed",
        type=_existing_path,
        required=True,
        help="Path to the fixed template T1w image.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path where the registered output image is written.",
    )
    return parser.parse_args()


def main() -> None:
    """Run ANTs registration from moving to fixed image."""
    args = parse_args()

    niwrap.use_auto()

    prefix = "t1w_to_template_"
    xfm = ants.ants_registration_sy_n_quick_sh(
        dimensionality=3,
        fixed_image=args.fixed,
        moving_image=args.moving,
        output_prefix=prefix,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(xfm.root / f"{prefix}Warped.nii.gz", args.output)


if __name__ == "__main__":
    main()
