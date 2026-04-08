# Xeno-Canto Data Curator

Prepares AudioMoth recordings of the California Red-legged Frog (*Rana draytonii*, RADR) for batch submission to [Xeno-canto](https://xeno-canto.org/).

## What it does

- Scans AudioMoth WAV clips for RADR-positive detections
- Parses recording metadata (date, time, site, quality, call type) directly from filenames
- Maps all fields to the official XC batch upload template format
- Outputs a submission-ready `xc_metadata.csv`
- Optionally bundles the WAV files into a flat ZIP for transfer to XC admins

## Usage

```bash
# Generate metadata CSV only
python src/pipeline.py

# Generate metadata CSV + ZIP of audio files
python src/pipeline.py --zip
```

Output is written to `output/` (gitignored).

## Project structure

```
src/
  constants.py        # Site registry, species info, XC field mappings
  filename_parser.py  # Parses AudioMoth filenames into structured metadata
  xc_formatter.py     # Maps parsed metadata to XC row format
  pipeline.py         # Entry point
docs/
  project_overview.md
  data_sources.md     # Recording sites, coordinates, filename conventions
  xc_batch_upload.md  # XC submission process and field reference
```

## Recording sites

| Site | Recorder(s) | Country |
|---|---|---|
| Wheatley Ranch | Moth01-04, 06 | United States |
| SRPER Cole Creek | Moth08 | United States |
| SRPER Sylvan Pond | Moth11, 12 | United States |
| Rancho Meling | Moth13 | Mexico |

## Requirements

Python 3.10+. No external dependencies required to run the pipeline.
