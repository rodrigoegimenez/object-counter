import os
from unittest.mock import patch, MagicMock

from counter import config


class TestCountDetectedObjects:
    @patch.dict(os.environ, {"ENV": "dev"})
    @patch("counter.config.FakeObjectDetector")
    def tests_gets_dev_prediction_action(self, fake_object_detector) -> None:
        config.get_prediction_action()
        fake_object_detector.assert_called()

    @patch.dict(
        os.environ, {
            "ENV": "prod",
            "TFS_HOST": "localhost",
            "TFS_PORT": "8501"
        }
    )
    @patch("counter.config.TFSObjectDetector")
    def tests_gets_prod_prediction_action(self, fake_object_detector: MagicMock) -> None:
        config.get_prediction_action()
        fake_object_detector.assert_called_with(host="localhost", port="8501")
