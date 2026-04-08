# Xeno-Canto Data Curator — Project Overview

## Purpose

This project aggregates and curates audio recordings of the California Red-legged Frog
(*Rana draytonii*, RADR) for bulk submission to [Xeno-canto](https://xeno-canto.org/).

The primary output is a metadata spreadsheet conforming to the XC batch upload template,
paired with the corresponding WAV files, ready to send to XC administrators.

## Scope

- **In scope:** RADR (California Red-legged Frog) positive detections only.
- **Out of scope:**
  - RACA (American Bullfrog, *Rana catesbeiana*) recordings — held in `All_Audio_Data/raca/`.
  - Negative/noise files — files in any `negative/` subfolder are excluded.

## Source Data

See [data_sources.md](data_sources.md) for the full breakdown of recording locations,
recorder hardware, filename conventions, and metadata fields.

## Pipeline

1. Parse positive RADR filenames to extract metadata (date, time, recorder ID, call type, quality).
2. Resolve recorder ID to site name, GPS coordinates, and elevation using the site registry.
3. Map internal field values to XC batch upload field values.
4. Output the XC-formatted metadata spreadsheet.
5. Bundle the WAV files for transfer to XC admins.

### Running the pipeline

```
python src/pipeline.py
```

Optional flags:

```
python src/pipeline.py --data-dir /path/to/splits --output /path/to/out.csv
```

Output is written to `output/xc_metadata.csv` by default.

### Source modules

| Module | Responsibility |
|---|---|
| `src/constants.py` | Site registry, species info, XC field mappings, output column list |
| `src/filename_parser.py` | Regex-based filename parsing -> `ParsedFilename` dataclass |
| `src/xc_formatter.py` | Maps `ParsedFilename` to an XC row dict |
| `src/pipeline.py` | Entry point: finds files, orchestrates parsing, writes CSV |

See [xc_batch_upload.md](xc_batch_upload.md) for XC submission requirements and field mappings.

## Submission Method

Batch upload via email to XC administrators. Metadata is submitted as a spreadsheet; audio
files are shared via a file-sharing service (e.g., WeTransfer or Dropbox). See
[xc_batch_upload.md](xc_batch_upload.md) for details.
