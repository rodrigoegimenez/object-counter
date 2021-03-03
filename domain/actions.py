from typing import List

from PIL import Image

from adapters.object_detector import ObjectDetector
from domain.models import Prediction
from domain.utils import draw


class CountDetectedObjects:
    def __init__(self, object_detector: ObjectDetector):
        self.__object_detector = object_detector

    def execute(self, image) -> List[Prediction]:
        predictions = self.__object_detector.predict(image)
        if __debug__:
            image = Image.open(image)
            draw(predictions, image)
        return predictions