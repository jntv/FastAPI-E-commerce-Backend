from tests.conftest import client, test_session


def test_user_registration(client, test_session):
    # Simulate user registration with valid data
    data = {"email": "test@example.com", "password": "secret123"}
    response = client.post("/api/auth/register", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}

    # Test registration with existing email
    response = client.post("/api/auth/register", json=data)
    assert response.status_code == 400
    assert "Email already exists" in response.json()["detail"]  # Check specific error message


def test_user_login(client, test_session):
    # Simulate user registration first (assuming a user exists)
    data = {"email": "test@example.com", "password": "secret123"}
    client.post("/api/auth/register", json=data)

    # Login with valid credentials
    data = {"username": "test@example.com", "password": "secret123"}
    response = client.post("/api/auth/login", data=data)
    assert response.status_code == 200
    # ... assert presence of JWT token in the response (implementation omitted)

    # Test login with invalid credentials
    data = {"username": "test@example.com", "password": "wrong_password"}
    response = client.post("/api/auth/login", data=data)
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]  # Check specific error message
