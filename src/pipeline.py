"""Main pipeline: generate the Xeno-Canto batch upload metadata CSV.

Scans the AudioMoth WAV clips directory for RADR-positive recordings, parses
each filename, maps metadata to Xeno-Canto format, and writes the result as a
CSV file ready for submission to XC administrators.

Usage (run from the project root):
    python src/pipeline.py
    python src/pipeline.py --data-dir /path/to/splits --output /path/to/out.csv
"""

import argparse
import csv
import logging
import pathlib
import sys
from typing import Iterator

# Allow running this file directly from the project root, with src/ on the path.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from constants import RADR_POSITIVE_LABEL, XC_OUTPUT_COLUMNS
from filename_parser import parse_filename
from xc_formatter import to_xc_row

# ---------------------------------------------------------------------------
# Default paths (resolved relative to this file so the script is location-
# independent regardless of the working directory).
# ---------------------------------------------------------------------------

_SRC_DIR = pathlib.Path(__file__).resolve().parent
_PROJECT_ROOT = _SRC_DIR.parent

DEFAULT_DATA_DIR = (
    _PROJECT_ROOT / "All_Audio_Data" / "from custom classifier suite" / "splits"
)
DEFAULT_OUTPUT_PATH = _PROJECT_ROOT / "output" / "xc_metadata.csv"

POSITIVE_SUBDIR_NAME = "positive"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Core steps
# ---------------------------------------------------------------------------


def find_positive_wav_files(splits_dir: pathlib.Path) -> Iterator[pathlib.Path]:
    """Yield WAV files located inside a 'positive' subdirectory.

    Walks the entire splits directory tree and returns only files whose
    immediate parent directory is named 'positive'.

    Args:
        splits_dir: Root of the splits directory tree.

    Yields:
        Path objects for each positive WAV file found.
    """
    for wav_file in splits_dir.rglob("*.wav"):
        if wav_file.parent.name.lower() == POSITIVE_SUBDIR_NAME:
            yield wav_file


def build_rows(
    splits_dir: pathlib.Path,
) -> tuple[list[dict], list[tuple[str, str]]]:
    """Parse all positive WAV files and produce XC metadata rows.

    Args:
        splits_dir: Root of the splits directory tree.

    Returns:
        A 2-tuple of:
          - rows: list of XC row dicts ready for CSV export.
          - errors: list of (filename, error_message) for files that failed.
    """
    rows: list[dict] = []
    errors: list[tuple[str, str]] = []

    for wav_path in find_positive_wav_files(splits_dir):
        try:
            parsed = parse_filename(wav_path.name)
            if parsed.label != RADR_POSITIVE_LABEL:
                log.warning(
                    "Unexpected label '%s' in positive/ directory: %s",
                    parsed.label,
                    wav_path.name,
                )
                continue
            rows.append(to_xc_row(parsed, wav_path.name))
        except (ValueError, KeyError) as exc:
            errors.append((wav_path.name, str(exc)))

    return rows, errors


def write_csv(rows: list[dict], output_path: pathlib.Path) -> None:
    """Write XC metadata rows to a CSV file.

    Args:
        rows: List of row dicts keyed by XC_OUTPUT_COLUMNS.
        output_path: Destination file path.

    Side effects:
        Creates parent directories as needed and writes the CSV file to disk.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=XC_OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Namespace with data_dir and output attributes.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Generate a Xeno-Canto batch upload metadata CSV "
            "from AudioMoth RADR-positive WAV clips."
        )
    )
    parser.add_argument(
        "--data-dir",
        type=pathlib.Path,
        default=DEFAULT_DATA_DIR,
        metavar="PATH",
        help=f"Path to the splits directory (default: {DEFAULT_DATA_DIR})",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=DEFAULT_OUTPUT_PATH,
        metavar="PATH",
        help=f"Output CSV path (default: {DEFAULT_OUTPUT_PATH})",
    )
    return parser.parse_args()


def main() -> int:
    """Run the pipeline and return a shell exit code.

    Returns:
        0 if all files were processed successfully.
        1 if the data directory was not found or any files could not be parsed.
    """
    args = _parse_args()

    if not args.data_dir.exists():
        log.error("Data directory not found: %s", args.data_dir)
        return 1

    rows, errors = build_rows(args.data_dir)
    write_csv(rows, args.output)
    log.info("Wrote %d rows to %s", len(rows), args.output)

    if errors:
        log.warning("%d file(s) could not be parsed:", len(errors))
        for filename, msg in errors:
            log.warning("  %s: %s", filename, msg)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
