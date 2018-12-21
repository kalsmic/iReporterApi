import pytest

from api.app import create_app



@pytest.fixture
def app():
    """Tells Flask that app is in test mode
    """
    app = create_app({'TESTING': True})

    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """ Tests will use the client to make requests to the
      application without running the server.
    """
    return app.test_client()
