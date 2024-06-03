from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pytest

# Replace with your actual database connection details for the test database
TEST_DATABASE_URL = "sqlite:///test_ecomm.db"  # Example for SQLite

# Create a separate engine for testing
test_engine = create_engine(TEST_DATABASE_URL)

# Create a global session fixture with automatic table recreation after each test
@pytest.fixture(scope="module")
def test_session():
    connection = test_engine.connect()
    transaction = connection.begin()
    yield sessionmaker(autocommit=False, autoflush=False, bind=test_engine)()
    transaction.rollback()
    connection.close()

# Create a global app fixture
@pytest.fixture(scope="module")
def test_app():
    # Replace with your actual application instance creation logic
    # Here's a simplified example assuming you have an app.py file
    from app import app
    return app

# Create a global FastAPI test client fixture
@pytest.fixture(scope="module")
def client(test_app):
    with TestClient(test_app) as c:
        yield c
