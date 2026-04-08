"""Parses AudioMoth WAV filenames into structured metadata.

Two filename conventions are supported:

  New data (Moth01-Moth12):
    {RecorderID}_{YYYYMMDD}_{HHMMSS}_{label}_{quality}_{call_type}[_dup{N}].wav

  Legacy data (Moth13 / Rancho Meling):
    {RecorderID}_{label}_{quality}_{call_type}[_dup{N}].wav

The filename is treated as the authoritative source for all per-recording metadata.
"""

import re
from dataclasses import dataclass
from typing import Optional


# Matches new-data filenames that include a date and time component.
_TIMESTAMPED_PATTERN = re.compile(
    r"^(?P<recorder_id>Moth\d+)"
    r"_(?P<date>\d{8})"
    r"_(?P<time>\d{6})"
    r"_(?P<label>positive|negative)"
    r"_(?P<quality>high|medium|low)"
    r"_(?P<call_type>grunt|growl|both)"
    r"(?:_dup\d+)?\.wav$",
    re.IGNORECASE,
)

# Matches legacy filenames that have no date or time component.
_LEGACY_PATTERN = re.compile(
    r"^(?P<recorder_id>Moth\d+)"
    r"_(?P<label>positive|negative)"
    r"_(?P<quality>high|medium|low)"
    r"_(?P<call_type>grunt|growl|both)"
    r"(?:_dup\d+)?\.wav$",
    re.IGNORECASE,
)

_DUP_MARKER = "_dup"


@dataclass(frozen=True)
class ParsedFilename:
    """Structured representation of metadata extracted from an AudioMoth WAV filename.

    Attributes:
        recorder_id: AudioMoth unit label, e.g. "Moth08".
        date: Recording date as YYYYMMDD string, or None for legacy files.
        time: Recording start time as HHMMSS string, or None for legacy files.
        label: Detection verdict; "positive" or "negative".
        quality: Assessed signal quality; "high", "medium", or "low".
        call_type: RADR vocalization type; "grunt", "growl", or "both".
        is_duplicate: True when the filename carries a _dupN suffix, indicating
            this clip shares a recorder-minute with at least one other clip.
    """

    recorder_id: str
    date: Optional[str]
    time: Optional[str]
    label: str
    quality: str
    call_type: str
    is_duplicate: bool


def parse_filename(filename: str) -> ParsedFilename:
    """Parse an AudioMoth WAV filename into a structured ParsedFilename.

    Tries the timestamped pattern first, then the legacy pattern.

    Args:
        filename: WAV basename only (not a full path).

    Returns:
        A ParsedFilename with all fields populated from the filename.

    Raises:
        ValueError: If the filename does not match either known pattern.
    """
    match = _TIMESTAMPED_PATTERN.match(filename)
    if match:
        return _build_parsed(match, has_timestamp=True, filename=filename)

    match = _LEGACY_PATTERN.match(filename)
    if match:
        return _build_parsed(match, has_timestamp=False, filename=filename)

    raise ValueError(
        f"Filename does not match any known AudioMoth pattern: {filename!r}"
    )


def _build_parsed(
    match: re.Match, *, has_timestamp: bool, filename: str
) -> ParsedFilename:
    """Construct a ParsedFilename from a successful regex match.

    Args:
        match: A successful regex match against a filename.
        has_timestamp: Whether the matched pattern includes date/time groups.
        filename: The original filename string, used to detect _dup suffix.

    Returns:
        A populated ParsedFilename dataclass.
    """
    groups = match.groupdict()
    return ParsedFilename(
        recorder_id=groups["recorder_id"],
        date=groups["date"] if has_timestamp else None,
        time=groups["time"] if has_timestamp else None,
        label=groups["label"].lower(),
        quality=groups["quality"].lower(),
        call_type=groups["call_type"].lower(),
        is_duplicate=_DUP_MARKER in filename.lower(),
    )
