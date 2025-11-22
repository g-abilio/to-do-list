import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True

    # using a temporary SQLite database in the RAM (test fake)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # using a simulated HTTP client that can interact with the application (test fake)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

        with app.app_context():
            db.drop_all()