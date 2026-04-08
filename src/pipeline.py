"""Main pipeline: generate the Xeno-Canto batch upload metadata CSV and
optionally bundle the corresponding WAV files into a ZIP for submission.

Scans the AudioMoth WAV clips directory for RADR-positive recordings, parses
each filename, maps metadata to Xeno-Canto format, and writes the result as a
CSV file ready for submission to XC administrators.

Usage (run from the project root):
    python src/pipeline.py
    python src/pipeline.py --zip
    python src/pipeline.py --data-dir /path/to/splits --output /path/to/out.csv --zip --zip-output /path/to/out.zip
"""

import argparse
import csv
import logging
import pathlib
import sys
import zipfile
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
DEFAULT_ZIP_PATH = _PROJECT_ROOT / "output" / "xc_audio.zip"

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


def build_zip(
    splits_dir: pathlib.Path, zip_path: pathlib.Path, rows: list[dict]
) -> None:
    """Bundle positive RADR WAV files into a flat ZIP archive.

    Only files whose filenames appear in the metadata rows are included,
    ensuring the ZIP and CSV are always in sync. Files are stored flat
    (no subdirectory structure) inside the ZIP, which is the format expected
    by Xeno-Canto for batch submission.

    Args:
        splits_dir: Root of the splits directory tree to search for WAV files.
        zip_path: Destination ZIP file path.
        rows: The metadata rows already produced by build_rows; used to
            determine which filenames to include.

    Side effects:
        Creates parent directories as needed and writes the ZIP file to disk.
        Logs a warning for any filename in rows whose WAV file cannot be found.
    """
    included = {row["filename"] for row in rows}
    wav_index: dict[str, pathlib.Path] = {
        p.name: p for p in find_positive_wav_files(splits_dir)
    }

    zip_path.parent.mkdir(parents=True, exist_ok=True)
    missing: list[str] = []

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_STORED) as zf:
        for filename in sorted(included):
            wav_path = wav_index.get(filename)
            if wav_path is None:
                missing.append(filename)
                continue
            zf.write(wav_path, arcname=filename)

    log.info("Wrote %d files to %s", len(included) - len(missing), zip_path)

    if missing:
        log.warning("%d file(s) listed in metadata but not found on disk:", len(missing))
        for name in missing:
            log.warning("  %s", name)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Namespace with data_dir, output, zip, and zip_output attributes.
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
    parser.add_argument(
        "--zip",
        action="store_true",
        help="Also bundle the positive WAV files into a ZIP archive for submission.",
    )
    parser.add_argument(
        "--zip-output",
        type=pathlib.Path,
        default=DEFAULT_ZIP_PATH,
        metavar="PATH",
        help=f"Output ZIP path (default: {DEFAULT_ZIP_PATH})",
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

    if args.zip:
        build_zip(args.data_dir, args.zip_output, rows)

    if errors:
        log.warning("%d file(s) could not be parsed:", len(errors))
        for filename, msg in errors:
            log.warning("  %s: %s", filename, msg)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
