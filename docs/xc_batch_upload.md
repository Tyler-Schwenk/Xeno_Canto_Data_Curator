# Xeno-Canto Batch Upload

## Submission Process

Batch uploads cannot be self-uploaded. The process is:

1. Prepare a metadata spreadsheet using the XC template (see below).
2. Bundle WAV files into a ZIP file.
3. Share the ZIP via a file-sharing service (WeTransfer, Dropbox, etc.).
4. Email the metadata spreadsheet and the sharing link to the XC contact address.
5. XC administrators check the metadata for errors and coordinate corrections before ingestion.

**Recommendation:** Submit a small pilot batch (up to 100 recordings) first to validate the
metadata format before submitting the full dataset.

---

## Metadata Spreadsheet Template

XC provides a template spreadsheet. The second tab is the metadata entry template; the
third tab shows formatting examples; the fourth tab lists predefined values for fixed fields.

### Required Fields

| XC Field           | Source in Our Data                              | Notes                                                     |
|--------------------|-------------------------------------------------|-----------------------------------------------------------|
| genus              | `Rana`                                          | Fixed value for RADR                                      |
| species            | `draytonii`                                     | Fixed value for RADR                                      |
| country            | `United States` or `Mexico`                     | Rancho Meling is in Mexico; all others are US             |
| location           | See site registry in data_sources.md            | Human-readable place name                                 |
| latitude           | See site registry in data_sources.md            | Decimal degrees, to be filled once GPS confirmed          |
| longitude          | See site registry in data_sources.md            | Decimal degrees, to be filled once GPS confirmed          |
| elevation          | See site registry in data_sources.md            | Meters above sea level                                    |
| date               | Parsed from filename (`YYYYMMDD`)               | Empty for Moth13 (OldData)                                |
| time               | Parsed from filename (`HHMMSS` -> `HH:MM`)      | Empty for Moth13 (OldData)                                |
| file_name          | Clip filename                                   | Must match the filename in the ZIP exactly                |
| license            | Predefined — see tab 4                          | To be decided; CC BY-NC-SA recommended                    |
| recording_type     | Predefined — see tab 4                          | `field recording`                                         |
| auto_recording     | Predefined — see tab 4                          | `yes` — all recordings are from passive AudioMoth units   |
| animal_seen        | Predefined — see tab 4                          | `no` — passive recorders, animal not observed             |
| playback_used      | Predefined — see tab 4                          | `no`                                                      |
| quality            | Mapped from `high`/`medium`/`low` (see below)  |                                                           |

### Optional but Recommended Fields

| XC Field    | Source in Our Data         | Notes                                                        |
|-------------|----------------------------|--------------------------------------------------------------|
| sound_type  | Mapped from `call_type`    | See mapping table below                                      |
| sex         | Not available              | Leave blank                                                  |
| life_stage  | Not available              | Leave blank                                                  |
| method      | `AudioMoth`                | Passive acoustic recorder                                    |
| remarks     | See comment template below |                                                              |

---

## Field Value Mappings

### Quality

| Internal value | XC quality value |
|----------------|-----------------|
| `high`         | `A`             |
| `medium`       | `B`             |
| `low`          | `C`             |

### Sound Type (call_type -> XC sound_type)

XC uses predefined values for amphibians. The correct values for RADR are to be confirmed
against XC tab 5-9 of the template spreadsheet. Tentative mappings:

| Internal call_type | XC sound_type (tentative) |
|--------------------|--------------------------|
| `grunt`            | `advertisement call`     |
| `growl`            | `advertisement call`     |
| `both`             | `advertisement call`     |

### Country by Site

| Site               | Country       |
|--------------------|---------------|
| Wheatley Ranch     | United States |
| SRPER Cole Creek   | United States |
| SRPER Sylvan Pond  | United States |
| Rancho Meling      | Mexico        |

---

## Remarks / Comments Template

XC values comments on recordings. For passive AudioMoth deployments the following
information should be included in the remarks field:

- Recorder hardware (AudioMoth, passive deployment)
- Clip is a 3-second segment extracted from a longer continuous recording
- Call type detected (grunt, growl, or both)
- Whether date/time is unavailable (for Moth13/OldData records)
- If multiple clips exist from the same recorder-minute, note they are sub-samples of the
  same individual or acoustic event (to prevent pseudo-replication)

---

## WAV Format Notes

XC now accepts WAV files directly (as of 2024). Do not convert to MP3 unless file size is
a concern for transfer. The full WAV files preserve maximum scientific value.

Clip duration is approximately 3 seconds, which meets XC's minimum clip guidelines.
