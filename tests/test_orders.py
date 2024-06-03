from tests.conftest import client, test_session


def test_create_order(client, test_session):
    # Simulate user registration (assuming a user exists)
    # ... (code to register a user if needed)

    # Login to get a JWT token
    data = {"username": "test@example.com", "password": "secret123"}
    login_response = client.post("/api/auth/login", data=data)
    access_token = login_response.json()["access_token"]  # Assuming JWT token is returned

    # Create a valid order with existing product ID
    product_id = 1  # Replace with an actual product ID
    order_data = {"user_email": "test@example.com", "items": [{"product_id": product_id, "quantity": 2}]}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/api/orders/", headers=headers, json=order_data)
    assert response.status_code == 200
    # ... assert presence of created order details in the response

def test_create_order_invalid_product(client, test_session):
    # Simulate user login
    # ... (code to login and get access token)
    headers = {"Authorization": f"Bearer {access_token}"}

    # Create order with non-existent product ID
    order_data = {"user_email": "test@example.com", "items": [{"product_id": 99, "quantity": 1}]}
    response = client.post("/api/orders/", headers=headers, json=order_data)
    assert response.status_code == 400  # Expect bad request for invalid product
    assert "Product not found" in response.json()["detail"]  # Check specific error message

def test_create_order_insufficient_quantity(client, test_session):
    # Simulate user login
    # ... (code to login and get access token)
    headers = {"Authorization": f"Bearer {access_token}"}

    # Create order with insufficient product quantity
    product_id = 1  # Replace with an actual product ID with limited quantity
    order_data = {"user_email": "test@example.com", "items": [{"product_id": product_id, "quantity": 10}]}
    response = client.post("/api/orders/", headers=headers, json=order_data)
    assert response.status_code == 400  # Expect bad request for insufficient quantity
    assert "Insufficient product quantity" in response.json()["detail"]  # Check specific error message

def test_get_order(client, test_session):
    # Simulate user registration and order creation (assuming an order exists)
    # ... (code to register a user, create a product, and place an order)

    # Get the created order by the user who placed it
    order_id = response.json()["id"]  # Replace with the actual order ID
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"/api/orders/{order_id}", headers=headers)
    assert response.status_code == 200
    # ... assert presence of retrieved order details in the response

def test_get_order_unauthorized(client):
    # Access order details without authorization
    response = client.get("/api/orders/1")  # Replace with an existing order ID
    assert response.status_code == 401  # Expect unauthorized without access token
