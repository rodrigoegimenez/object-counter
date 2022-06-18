import pytest

from counter.entrypoints.webapp import app


@pytest.fixture(scope="module")
def test_client():
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client
