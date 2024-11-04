def test_login_page(client):
    response = client.get("/")
    assert response.status_code == 200
    #An example for future implementations
    assert b"Dumps" in response.data

def test_homepage(client):
    response = client.get("/import")
    assert response.status_code == 200
    #An example for future implementations
    assert b"Import" in response.data

def test_about_page(client):
    response = client.get("/about")
    assert response.status_code == 200
    #An example for future implementations
    assert b"PGImporter" in response.data

def test_config_page(client):
    response = client.get("/configs")
    assert response.status_code == 200
    assert b"Configuration" in response.data