import os

from counter.adapters.count_repo import CountMongoDBRepo, CountInMemoryRepo, CountPostgresDBRepo
from counter.adapters.object_detector import TFSObjectDetector, FakeObjectDetector
from counter.domain.actions import CountDetectedObjects, PredictObjects


def dev_count_action() -> CountDetectedObjects:
    return CountDetectedObjects(FakeObjectDetector(), CountInMemoryRepo())


def prod_count_action() -> CountDetectedObjects:
    tfs_host = os.environ.get('TFS_HOST', 'localhost')
    tfs_port = os.environ.get('TFS_PORT', 8501)
    db_engine = os.environ.get("DB_ENGINE", "mongo")
    detector = TFSObjectDetector(tfs_host, tfs_port)
    if db_engine == "mongo":
        mongo_host = os.environ.get('MONGO_HOST', 'localhost')
        mongo_port = os.environ.get('MONGO_PORT', 27017)
        mongo_db = os.environ.get('MONGO_DB', 'prod_counter')
        db_repo = CountMongoDBRepo(host=mongo_host, port=mongo_port, database=mongo_db)
    elif db_engine == "postgres":
        postgres_host = os.environ.get('POSTGRES_HOST', 'localhost')
        postgres_port = os.environ.get('POSTGRES_PORT', 5432)
        postgres_db = os.environ.get('POSTGRES_DB', 'prod_counter')
        postgres_user = os.environ.get('POSTGRES_USER', 'postgres')
        postgres_password = os.environ.get('POSTGRES_PASSWORD', 'postgres')
        db_repo = CountPostgresDBRepo(host=postgres_host, port=postgres_port, database=postgres_db,
                                       user=postgres_user, password=postgres_password)

    else:
        raise ValueError("Unknown database engine %s" % db_engine)

    return CountDetectedObjects(detector, db_repo)


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