from dataclasses import dataclass
from enum import Enum


@dataclass
class GeoResult:
    pmid: str
    affiliation: str
    lat: float
    lng: float
    confidence: "Confidence"
    index: int


class Confidence(Enum):
    UNSPECIFIED = 0
    NO_RESULT = 1
    LOW = 10
    MEDIUM = 20
    HIGH = 30
