from tests.conftest import client, test_session


def test_get_all_products(client):
    response = client.get("/api/products/")
    assert response.status_code == 200
    # ... assert presence of product data in the response (assuming products exist)


def test_create_product(client, test_session):
    data = {"name": "Test Product", "description": "This is a test product", "price": 19.99, "quantity": 10}
    response = client.post("/api/products/", json=data)
    assert response.status_code == 200
    # ... assert presence of created product details in the response


def test_update_product(client, test_session):
    # Create a product first
    data = {"name": "Test Product", "description": "This is a test product", "price": 19.99, "quantity": 10}
    response = client.post("/api/products/", json=data)
    product_id = response.json()["id"]

    # Update product details
    update_data = {"name": "Updated Product Name", "price": 24.99}
    
