from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json


@dataclass
class Box:
    xmin: float
    ymin: float
    xmax: float
    ymax: float


@dataclass
class Prediction:
    class_name: str
    score: float
    box: Box


@dataclass
class ObjectCount:
    object_class: str
    count: int


@dataclass_json
@dataclass
class CountResponse:
    current_objects: List[ObjectCount]
    total_objects: List[ObjectCount]


@dataclass_json
@dataclass
class PredictionResponse:
    predictions: List[Prediction]
