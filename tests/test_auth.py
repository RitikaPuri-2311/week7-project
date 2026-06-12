def test_login_success(test_client):
    # FIRST create user
    test_client.post("/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "test123",
        "role_id": 1
    })

    # THEN login
    response = test_client.post("/login", json={
        "email": "test@example.com",
        "password": "test123"
    })

    assert response.status_code == 200

def test_login_wrong_password(test_client):
    response = test_client.post("/login", json={
        "email": "test@example.com",
        "password": "wrongpass"
    })

    assert response.status_code == 401

def test_logout(test_client):
    response = test_client.post("/logout", json={
        "user_id": 1
    })

    assert response.status_code == 200