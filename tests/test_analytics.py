def test_user_analytics(test_client):
    response = test_client.get("/analytics/users")

    assert response.status_code == 200
    assert "total_users" in response.json()
    assert "active_users" in response.json()

def test_activity_analytics(test_client):
    response = test_client.get("/analytics/activity")

    assert response.status_code == 200
    assert isinstance(response.json(), list)