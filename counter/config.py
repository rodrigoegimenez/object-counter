import os

from counter.adapters.count_repo import CountMongoDBRepo, CountInMemoryRepo
from counter.adapters.object_detector import TFSObjectDetector, FakeObjectDetector
from counter.domain.actions import CountDetectedObjects, PredictObjects


def dev_count_action() -> CountDetectedObjects:
    return CountDetectedObjects(FakeObjectDetector(), CountInMemoryRepo())


def prod_count_action() -> CountDetectedObjects:
    tfs_host = os.environ.get('TFS_HOST', 'localhost')
    tfs_port = os.environ.get('TFS_PORT', 8501)
    mongo_host = os.environ.get('MONGO_HOST', 'localhost')
    mongo_port = os.environ.get('MONGO_PORT', 27017)
    mongo_db = os.environ.get('MONGO_DB', 'prod_counter')
    return CountDetectedObjects(TFSObjectDetector(tfs_host, tfs_port, 'rfcn'),
                                CountMongoDBRepo(host=mongo_host, port=mongo_port, database=mongo_db))


def get_count_action() -> CountDetectedObjects:
    env = os.environ.get('ENV', 'dev')
    count_action_fn = f"{env}_count_action"
    return globals()[count_action_fn]()


def dev_prediction_action() -> PredictObjects:
    return PredictObjects(FakeObjectDetector())


def prod_prediction_action() -> PredictObjects:
    tfs_host = os.environ.get('TFS_HOST', 'localhost')
    tfs_port = os.environ.get('TFS_PORT', 8501)
    return PredictObjects(TFSObjectDetector(host=tfs_host, port=tfs_port))


def get_prediction_action():
    env = os.environ.get('ENV', 'dev')
    return action_functions_mapper[f"{env}_prediction_action"]()


action_functions_mapper = {
    "dev_prediction_action": dev_prediction_action,
    "prod_prediction_action": prod_prediction_action,
}