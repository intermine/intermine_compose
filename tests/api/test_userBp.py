
def test_register(client):
    resp = client.post(
        "/api/v1/user/register",
        json={
            "email": "john@doe.me",
	        "password": "superpass",
	        "firstName": "John",
	        "lastName": "Doe",
	        "organisation": "InterMine"
        }
    )
    assert resp.status_code == 200

def test_login(client):
    resp = client.post(
        "/api/v1/user/login",
        json={
            "email": "john@doe.me",
            "password": "superpass"
        }
    )
    assert resp.status_code == 200

def test_get_profile(client):
    resp = client.get(
        "api/v1/user/profile"
    )
    assert resp.status_code == 200
    assert resp.get_json() == {
        "email": "test@user.me",
	    "firstName": "Bruce",
	    "lastName": "Stark",
	    "organisation": "InterMine"
    }

def test_update_profile(client):
    resp = client.post(
        "api/v1/user/profile",
        json={
	        "firstName": "JohnNew",
	        "lastName": "DoeNew",
	        "organisation": "InterMineNew"
        }
    )
    assert resp.status_code == 200
    resp = client.get(
        "api/v1/user/profile"
    )
    assert resp.status_code == 200
    assert resp.get_json() == {
        "email": "test@user.me",
	    "firstName": "JohnNew",
	    "lastName": "DoeNew",
	    "organisation": "InterMineNew"
    }



def test_logout(client):
    resp = client.get(
        "api/v1/user/logout"
    )
    assert resp.status_code == 200
