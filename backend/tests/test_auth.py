from tests.conftest import PASSWORD, make_user


def test_root_does_not_expose_database(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register_then_login_then_me(client):
    response = client.post(
        "/auth/register",
        json={"email": "new@example.com", "password": PASSWORD},
    )
    assert response.status_code == 200
    assert response.json()["role"] == "OPERATOR"
    assert "password" not in response.text

    login = client.post(
        "/auth/login",
        json={"email": "new@example.com", "password": PASSWORD},
    )
    token = login.json()["access_token"]

    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "new@example.com"


def test_register_rejects_short_password(client):
    response = client.post(
        "/auth/register",
        json={"email": "new@example.com", "password": "court"},
    )
    assert response.status_code == 422


def test_login_wrong_password(client, db):
    make_user(db, "a@example.com")
    response = client.post(
        "/auth/login", json={"email": "a@example.com", "password": "mauvais"}
    )
    assert response.status_code == 401


def test_protected_route_requires_token(client):
    assert client.get("/campaigns/").status_code == 401
    assert client.get(
        "/campaigns/", headers={"Authorization": "Bearer invalide"}
    ).status_code == 401


def test_admin_route_forbidden_for_operator(client, operator_headers):
    response = client.get("/auth/admin-test", headers=operator_headers)
    assert response.status_code == 403


def test_admin_route_ok_for_admin(client, admin_headers):
    assert client.get("/auth/admin-test", headers=admin_headers).status_code == 200
