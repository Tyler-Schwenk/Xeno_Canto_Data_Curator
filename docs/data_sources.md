# Data Sources

## Audio Files

All RADR-positive audio files are WAV format, recorded on **AudioMoth** passive acoustic
recorders. Files are 3-second clips segmented from longer continuous recordings.

### File Location

All positive RADR clips live under:

```
All_Audio_Data/from custom classifier suite/splits/
```

Organized into train/val/test_iid/test_ood splits, each with a `positive/` subfolder.
Only files in `positive/` subfolders are relevant for XC submission.

---

## Filename Convention

The filename is the authoritative source for per-recording metadata.

### New Data (Moth01–Moth12): With Timestamp

```
{RecorderID}_{YYYYMMDD}_{HHMMSS}_{label}_{quality}_{call_type}[_dup{N}].wav
```

| Component   | Example              | Description                                      |
|-------------|----------------------|--------------------------------------------------|
| RecorderID  | `Moth08`             | Identifies the physical AudioMoth unit and site  |
| YYYYMMDD    | `20250405`           | Recording date (local time)                      |
| HHMMSS      | `002000`             | Recording start time (local time, 24-hour)       |
| label       | `positive`           | RADR detection verdict                           |
| quality     | `high`/`medium`/`low`| Signal quality of the RADR call                 |
| call_type   | `grunt`/`growl`/`both`| Type of RADR vocalization present               |
| _dup{N}     | `_dup1` (optional)   | Distinguishes multiple clips from the same minute |

### Old Data (Moth13 / Rancho Meling): No Timestamp

```
{RecorderID}_{label}_{quality}_{call_type}[_dup{N}].wav
```

Moth13 files originate from a legacy dataset and do not contain timestamp information in
their filenames. Date and time fields will be empty in the XC submission for these records.

---

## Manifest CSV

`All_Audio_Data/from custom classifier suite/manifest.csv` contains pre-parsed metadata
for all files (positive and negative). Columns:

| Column         | Description                                                   |
|----------------|---------------------------------------------------------------|
| filename       | Clip filename (WAV)                                           |
| orig_full_path | Absolute path to the source file before renaming             |
| new_full_path  | Relative path within the splits directory                     |
| dataset        | `NewData` or `OldData`                                        |
| site           | Human-readable site name                                      |
| recorder       | Recorder label (e.g., `Moth08`)                               |
| recorder_id    | Numeric ID                                                    |
| label          | `positive` or `negative`                                      |
| quality        | `high`, `medium`, or `low`                                    |
| call_type      | `grunt`, `growl`, or `both`                                   |
| date           | Populated only for NewData; empty for OldData (Moth13)        |
| time           | Populated only for NewData; empty for OldData (Moth13)        |
| notes          | Free-text notes (often empty)                                 |
| date_filled    | (Internal field, not used for XC)                             |
| split          | `train`, `val`, `test_iid`, or `test_ood`                     |

---

## Recording Sites and Recorders

All recorders at the same named site share one GPS coordinate. Individual recorders within
a site were not given distinct positions.

| Recorder | Site Name          | Lat (DD)    | Lon (DD)     | Elevation (m) |
|----------|--------------------|-------------|--------------|---------------|
| Moth01   | Wheatley Ranch     | 33.212408   | -116.746651  | 949.1         |
| Moth02   | Wheatley Ranch     | 33.212408   | -116.746651  | 949.1         |
| Moth03   | Wheatley Ranch     | 33.212408   | -116.746651  | 949.1         |
| Moth04   | Wheatley Ranch     | 33.212408   | -116.746651  | 949.1         |
| Moth06   | Wheatley Ranch     | 33.212408   | -116.746651  | 949.1         |
| Moth08   | SRPER Cole Creek   | 33.531385   | -117.268689  | 540           |
| Moth11   | SRPER Sylvan Pond  | 33.529285   | -117.285871  | 573           |
| Moth12   | SRPER Sylvan Pond  | 33.529285   | -117.285871  | 573           |
| Moth13   | Rancho Meling      | 30.975073   | -115.744407  | 638.4         |

### Site Abbreviations

- **SRPER** — Santa Rosa Plateau Ecological Reserve
- **Rancho Meling** — Rancho Meling, Baja California, Mexico

---

## Hardware

| Field        | Value                  |
|--------------|------------------------|
| Recorder     | AudioMoth              |
| Manufacturer | Open Acoustic Devices  |
| File format  | WAV                    |
| Clip duration | ~3 seconds            |

Specific AudioMoth firmware version and sample rate settings are not yet recorded.
If available, these should be added here and included in XC submission comments.

---

## Excluded Data

- `All_Audio_Data/raca/` — American Bullfrog (*Rana catesbeiana*) recordings. Not submitted.
- Any `negative/` subfolder — clips containing noise or no RADR vocalization. Not submitted.
