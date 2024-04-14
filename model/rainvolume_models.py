# package: model
# rainvolume_models.py

from dataclasses import dataclass, field

@dataclass
class RainVolume:
    place: str
    this_year: int
    past_span: int
    rainvolume_days: list[list[float]] = field(default_factory=list)

@dataclass
class RainVolumeProbability:
    place: str
    this_year: int
    past_span: int
    day_span: int
    rainvolume_probabilities: dict = field(default_factory=dict)

@dataclass
class RainVolumeScore:
    place: str
    this_year: int
    past_span: int
    day_span: int
    rainvolume_scores: list[tuple] = field(default_factory=list)