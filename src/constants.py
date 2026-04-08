"""Central registry for all constants, site metadata, and field mappings
used in the Xeno-Canto batch upload pipeline.

All magic values, site coordinates, and XC field mappings live here.
When adding new recording sites or recorders, update SITE_REGISTRY only.
"""

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Species
# ---------------------------------------------------------------------------

SPECIES_GENUS = "Rana"
SPECIES_EPITHET = "draytonii"
RADR_POSITIVE_LABEL = "positive"

# ---------------------------------------------------------------------------
# Hardware
# ---------------------------------------------------------------------------

RECORDER_HARDWARE = "AudioMoth"
CLIP_DURATION_SECONDS = 3

# ---------------------------------------------------------------------------
# XC fixed field values
# ---------------------------------------------------------------------------

# 'type' field: valid values are 'single species' or 'soundscape'
RECORDING_TYPE = "single species"
# 'recording method' field: valid anuran values are 'field recording', 'in the hand', 'unknown'
RECORDING_METHOD = "field recording"
AUTO_RECORDING = "yes"
ANIMAL_SEEN = "no"
PLAYBACK_USED = "no"
# Full license name as required by XC predefined list
DEFAULT_LICENSE = "Creative Commons Attribution-NonCommercial 4.0"
RECORDIST_NAME = "Tyler Schwenk"

# XC placeholder for unknown date/time components
UNKNOWN_DATE = "????-??-??"
UNKNOWN_TIME = "??:??"

# ---------------------------------------------------------------------------
# Site registry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SiteInfo:
    """GPS and administrative metadata for a single recording site.

    Attributes:
        site: Human-readable site name used in XC location field.
        lat: Latitude in decimal degrees (WGS84).
        lon: Longitude in decimal degrees (WGS84).
        elevation_m: Elevation above sea level in metres.
        country: Full country name as expected by XC.
    """

    site: str
    lat: float
    lon: float
    elevation_m: float
    country: str


SITE_REGISTRY: dict[str, SiteInfo] = {
    "Moth01": SiteInfo(
        site="Wheatley Ranch",
        lat=33.212408,
        lon=-116.746651,
        elevation_m=949.1,
        country="United States",
    ),
    "Moth02": SiteInfo(
        site="Wheatley Ranch",
        lat=33.212408,
        lon=-116.746651,
        elevation_m=949.1,
        country="United States",
    ),
    "Moth03": SiteInfo(
        site="Wheatley Ranch",
        lat=33.212408,
        lon=-116.746651,
        elevation_m=949.1,
        country="United States",
    ),
    "Moth04": SiteInfo(
        site="Wheatley Ranch",
        lat=33.212408,
        lon=-116.746651,
        elevation_m=949.1,
        country="United States",
    ),
    "Moth06": SiteInfo(
        site="Wheatley Ranch",
        lat=33.212408,
        lon=-116.746651,
        elevation_m=949.1,
        country="United States",
    ),
    "Moth08": SiteInfo(
        site="SRPER Cole Creek",
        lat=33.531385,
        lon=-117.268689,
        elevation_m=540.0,
        country="United States",
    ),
    "Moth11": SiteInfo(
        site="SRPER Sylvan Pond",
        lat=33.529285,
        lon=-117.285871,
        elevation_m=573.0,
        country="United States",
    ),
    "Moth12": SiteInfo(
        site="SRPER Sylvan Pond",
        lat=33.529285,
        lon=-117.285871,
        elevation_m=573.0,
        country="United States",
    ),
    "Moth13": SiteInfo(
        site="Rancho Meling",
        lat=30.975073,
        lon=-115.744407,
        elevation_m=638.4,
        country="Mexico",
    ),
}

# ---------------------------------------------------------------------------
# Value mappings: internal -> XC
# ---------------------------------------------------------------------------

QUALITY_TO_XC: dict[str, str] = {
    "high": "A",
    "medium": "B",
    "low": "C",
}

CALL_TYPE_TO_XC_SOUND_TYPE: dict[str, str] = {
    "grunt": "advertisement call",
    "growl": "advertisement call",
    "both": "advertisement call",
}

# ---------------------------------------------------------------------------
# Output CSV column order (must match XC batch upload template)
# ---------------------------------------------------------------------------

# Column names and order must match the XC batch upload template exactly.
XC_OUTPUT_COLUMNS: list[str] = [
    "filename",
    "latitude",
    "longitude",
    "country",
    "location name",
    "elevation",
    "recording date",
    "time of day",
    "license",
    "recordist name",
    "recording device",
    "microphone",
    "type",
    "automatic recording",
    "genus",
    "species",
    "subspecies",
    "sex(es)",
    "life stage(s)",
    "animal seen?",
    "sound type(s)",
    "recording method",
    "collection date",
    "playback used?",
    "temperature",
    "background species",
    "collection specimen reference",
    "remarks",
    "quality",
]
