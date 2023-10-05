import pytest
from pytest_mock import MockFixture

@pytest.fixture
def client():
    app.config.update({"TESTING": True})

    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    #An example for future implementations
    assert b"Dumps" in response.data

def test_homepage(client):
    response = client.get("/import")
    assert response.status_code == 200
    #An example for future implementations
    assert b"Import" in response.data

def test_about_page(client):
    response = client.get("/about")
    assert response.status_code == 200
    #An example for future implementations
    assert b"PGImporter" in response.data