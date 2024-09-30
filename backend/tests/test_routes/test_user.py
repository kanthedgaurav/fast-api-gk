def test_create_user(client):
    data = {"email": "gauravkanthedgmail.com", "password": "password"}
    response = client.post("/users/", json=data)
    assert response.status_code == 201
    assert response.json()["email"] == "gauravkanthed@gmail.com"
