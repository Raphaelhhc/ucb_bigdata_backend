# package: model
# temperature_models.py

from dataclasses import dataclass, field

@dataclass
class Temperature:
    place: str
    this_year: int
    past_span: int
    temperature_days: list[list[float]] = field(default_factory=list)

@dataclass
class TemperatureProbability:
    place: str
    this_year: int
    past_span: int
    day_span: int
    temperature_probabilities: dict = field(default_factory=dict)

@dataclass
class TemperatureScore:
    place: str
    this_year: int
    past_span: int
    day_span: int
    temperature_scores: list[tuple] = field(default_factory=list)
