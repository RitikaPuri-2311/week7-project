def test_register_user(test_client):
    response = test_client.post("/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "test123",
        "role_id": 1
    })

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"

def test_duplicate_email(test_client):
    response = test_client.post("/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "test123",
        "role_id": 1
    })

    assert response.status_code == 409