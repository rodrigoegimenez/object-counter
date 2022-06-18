from pathlib import Path


def test_home_page_provides_swagger_ui(test_client):
    response = test_client.get("/")
    assert "Swagger" in response.text


resources = Path(__file__).parent.parent.parent / "resources"


def test_counting_using_fake_detector(test_client):
    response = test_client.post(
        "/object-count",
        data={
            "file": (resources / "images" / "boy.jpg").open("rb"),
        },
    )
    assert response.status_code == 200
