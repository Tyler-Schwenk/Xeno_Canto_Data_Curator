"""Converts parsed AudioMoth filename metadata into Xeno-Canto batch upload rows.

Each function in this module is intentionally pure (no side effects) so that
the formatting logic can be tested independently of the pipeline.
"""

from typing import Optional

from constants import (
    ANIMAL_SEEN,
    AUTO_RECORDING,
    CALL_TYPE_TO_XC_SOUND_TYPE,
    CLIP_DURATION_SECONDS,
    DEFAULT_LICENSE,
    PLAYBACK_USED,
    QUALITY_TO_XC,
    RECORDER_HARDWARE,
    RECORDING_METHOD,
    RECORDING_TYPE,
    RECORDIST_NAME,
    SITE_REGISTRY,
    SPECIES_EPITHET,
    SPECIES_GENUS,
    UNKNOWN_DATE,
    UNKNOWN_TIME,
)
from filename_parser import ParsedFilename


def to_xc_row(parsed: ParsedFilename, filename: str) -> dict:
    """Convert parsed filename metadata into a Xeno-Canto batch upload row dict.

    Args:
        parsed: Structured metadata extracted from the WAV filename.
        filename: The WAV basename used as the XC file_name field value.

    Returns:
        A dict keyed by XC_OUTPUT_COLUMNS whose values are ready for CSV export.

    Raises:
        KeyError: If parsed.recorder_id is not present in SITE_REGISTRY.
        KeyError: If parsed.quality or parsed.call_type has no XC mapping.
    """
    site = SITE_REGISTRY[parsed.recorder_id]
    return {
        "filename": filename,
        "latitude": site.lat,
        "longitude": site.lon,
        "country": site.country,
        "location name": site.site,
        "elevation": site.elevation_m,
        "recording date": _format_date(parsed.date),
        "time of day": _format_time(parsed.time),
        "license": DEFAULT_LICENSE,
        "recordist name": RECORDIST_NAME,
        "recording device": RECORDER_HARDWARE,
        "microphone": "",
        "type": RECORDING_TYPE,
        "automatic recording": AUTO_RECORDING,
        "genus": SPECIES_GENUS,
        "species": SPECIES_EPITHET,
        "subspecies": "",
        "sex(es)": "",
        "life stage(s)": "",
        "animal seen?": ANIMAL_SEEN,
        "sound type(s)": CALL_TYPE_TO_XC_SOUND_TYPE[parsed.call_type],
        "recording method": RECORDING_METHOD,
        "collection date": "",
        "playback used?": PLAYBACK_USED,
        "temperature": "",
        "background species": "",
        "collection specimen reference": "",
        "remarks": _build_remarks(parsed),
        "quality": QUALITY_TO_XC[parsed.quality],
    }


def _format_date(date_str: Optional[str]) -> str:
    """Convert a YYYYMMDD string to YYYY-MM-DD, or return the XC unknown placeholder.

    Args:
        date_str: Eight-digit date string, or None.

    Returns:
        ISO-formatted date string, or UNKNOWN_DATE if input is None.
    """
    if not date_str:
        return UNKNOWN_DATE
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"


def _format_time(time_str: Optional[str]) -> str:
    """Convert a HHMMSS string to HH:MM, or return the XC unknown placeholder.

    Args:
        time_str: Six-digit time string, or None.

    Returns:
        HH:MM formatted time string, or UNKNOWN_TIME if input is None.
    """
    if not time_str:
        return UNKNOWN_TIME
    return f"{time_str[:2]}:{time_str[2:4]}"


def _build_remarks(parsed: ParsedFilename) -> str:
    """Build the XC remarks field text for a single recording.

    Includes hardware context, clip provenance, and any caveats about
    data availability or pseudo-replication.

    Args:
        parsed: Structured metadata extracted from the WAV filename.

    Returns:
        A plain-text remarks string suitable for the XC comments field.
    """
    parts = [
        f"Passive {RECORDER_HARDWARE} deployment.",
        f"{CLIP_DURATION_SECONDS}-second clip extracted from a longer continuous recording.",
        f"Vocalization type: {parsed.call_type}.",
        f"Recorder unit: {parsed.recorder_id}.",
    ]

    if parsed.is_duplicate:
        parts.append(
            "Multiple clips share this recorder-minute and are sub-samples of the same "
            "acoustic event; they should not be treated as independent samples."
        )

    if parsed.date is None:
        parts.append(
            "Recording date and time are unavailable for this legacy dataset."
        )

    return " ".join(parts)
