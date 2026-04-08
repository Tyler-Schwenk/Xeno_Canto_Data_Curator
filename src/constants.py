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
        elevation_m: Elevation in whole metres above sea level (XC requires integer).
        country: Full country name as expected by XC.
        recordist: Name or institution to credit as recordist on XC.
    """

    site: str
    lat: float
    lon: float
    elevation_m: int
    country: str
    recordist: str


# TODO: Confirm the correct recordist name or institution for each recorder.
# Moth13 is legacy data from Frank; all others are Tyler Schwenk's deployments.
SITE_REGISTRY: dict[str, SiteInfo] = {
    "Moth01": SiteInfo(
        site="Wheatley Ranch",
        lat=33.212408,
        lon=-116.746651,
        elevation_m=949,
        country="United States",
        recordist="San Diego Natural History Museum",
    ),
    "Moth02": SiteInfo(
        site="Wheatley Ranch",
        lat=33.212408,
        lon=-116.746651,
        elevation_m=949,
        country="United States",
        recordist="San Diego Natural History Museum",
    ),
    "Moth03": SiteInfo(
        site="Wheatley Ranch",
        lat=33.212408,
        lon=-116.746651,
        elevation_m=949,
        country="United States",
        recordist="San Diego Natural History Museum",
    ),
    "Moth04": SiteInfo(
        site="Wheatley Ranch",
        lat=33.212408,
        lon=-116.746651,
        elevation_m=949,
        country="United States",
        recordist="San Diego Natural History Museum",
    ),
    "Moth06": SiteInfo(
        site="Wheatley Ranch",
        lat=33.212408,
        lon=-116.746651,
        elevation_m=949,
        country="United States",
        recordist="San Diego Natural History Museum",
    ),
    "Moth08": SiteInfo(
        site="SRPER Cole Creek",
        lat=33.531385,
        lon=-117.268689,
        elevation_m=540,
        country="United States",
        recordist="San Diego Natural History Museum",
    ),
    "Moth11": SiteInfo(
        site="SRPER Sylvan Pond",
        lat=33.529285,
        lon=-117.285871,
        elevation_m=573,
        country="United States",
        recordist="San Diego Natural History Museum",
    ),
    "Moth12": SiteInfo(
        site="SRPER Sylvan Pond",
        lat=33.529285,
        lon=-117.285871,
        elevation_m=573,
        country="United States",
        recordist="San Diego Natural History Museum",
    ),
    "Moth13": SiteInfo(
        site="Rancho Meling",
        lat=30.975073,
        lon=-115.744407,
        elevation_m=638,
        country="Mexico",
        recordist="San Diego Natural History Museum",
    ),
}

# ---------------------------------------------------------------------------
# Value mappings: internal -> XC
# ---------------------------------------------------------------------------

QUALITY_TO_XC: dict[str, str] = {
    "high": "A",
    "medium": "C",
    "low": "E",
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
