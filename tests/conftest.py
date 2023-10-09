import pytest, sys

#sys.path.append('../pgimporter') 

from pgimporter_app.app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

