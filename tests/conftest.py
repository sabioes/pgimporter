import pytest
from pgimporter_app.webapp import app

@pytest.fixture
def app():
    app = app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()