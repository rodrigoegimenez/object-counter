import pytest
from testcontainers.mongodb import MongoDbContainer

from counter.adapters.count_repo import CountMongoDBRepo
from counter.domain.models import ObjectCount


class TestCountMongoDbRepo:
    @pytest.fixture
    def mongodb_container(self):
        with MongoDbContainer() as container:
            yield container

    @pytest.fixture
    def mongodb_repo(self, mongodb_container):
        print(mongodb_container.MONGO_DB)
        host = mongodb_container.get_container_host_ip()
        port = int(mongodb_container.get_exposed_port(27017))
        database = mongodb_container.MONGO_DB
        repo = CountMongoDBRepo(host, port, database, "test", "test")
        yield repo

    @pytest.fixture
    def mongodb_client(self, mongodb_container):
        yield mongodb_container.get_connection_client()

    def test_reads_values(self, mongodb_client, mongodb_repo):
        # Arrange
        values = [
            ObjectCount(object_class="cat", count=1),
            ObjectCount(object_class="dog", count=3),
        ]
        mongodb_client.test.counter.insert_many(
            [{"object_class": v.object_class, "count": v.count} for v in values]
        )

        # Act
        read_values = mongodb_repo.read_values()

        # Assert
        assert values == read_values

    def test_writes_values(self, mongodb_client, mongodb_repo):
        # Arrange
        values = [
            ObjectCount(object_class="cat", count=1),
            ObjectCount(object_class="dog", count=3),
        ]

        # Act
        mongodb_repo.update_values(values)
        updated_values = mongodb_client.test.counter.find({})

        # Assert
        assert values == [
            ObjectCount(v["object_class"], v["count"]) for v in updated_values
        ]
