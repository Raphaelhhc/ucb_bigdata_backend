# model/recommend_models.py

from dataclasses import dataclass, field

@dataclass
class RecommendDate:
    place: str
    this_year: int
    past_span: int
    day_span: int
    recommend_date: list[tuple] = field(default_factory=list)
    recommend_date_probability: list[list[dict]] = field(default_factory=list)