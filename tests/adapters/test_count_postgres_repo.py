import pytest
import sqlalchemy
from testcontainers.postgres import PostgresContainer

from counter.adapters.count_repo import CountPostgresDBRepo
from counter.domain.models import ObjectCount


class TestCountMongoDbRepo:
    @pytest.fixture
    def postgres_container(self):
        with PostgresContainer() as container:
            yield container

    @pytest.fixture
    def postgres_repo(self, postgres_container):
        host = postgres_container.get_container_host_ip()
        port = int(postgres_container.get_exposed_port(5432))
        database = postgres_container.POSTGRES_DB
        user = postgres_container.POSTGRES_USER
        password = postgres_container.POSTGRES_PASSWORD
        repo = CountPostgresDBRepo(host, port, database, user, password)

        yield repo

    @pytest.fixture
    def postgres_client(self, postgres_container):
        yield sqlalchemy.create_engine(postgres_container.get_connection_url())

    def test_reads_values(self, postgres_client, postgres_repo):
        # Arrange
        values = [
            ObjectCount(object_class="cat", count=1),
            ObjectCount(object_class="dog", count=3),
        ]
        insert_query = (
            "INSERT INTO object_count VALUES "
            "(DEFAULT, 'cat', 1), (DEFAULT, 'dog', 3);"
        )
        postgres_client.execute(insert_query)

        # Act
        read_values = postgres_repo.read_values()

        # Assert
        assert values == read_values

    def test_writes_values(self, postgres_client, postgres_repo):
        # Arrange
        values = [
            ObjectCount(object_class="cat", count=1),
            ObjectCount(object_class="dog", count=3),
        ]

        # Act
        postgres_repo.update_values(values)
        updated_values = postgres_client.execute("SELECT * FROM object_count;")

        # Assert
        assert values == [ObjectCount(v[1], v[2]) for v in updated_values]
