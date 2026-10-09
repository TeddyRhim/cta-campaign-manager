PAYLOAD = {
    "first_name": "Ada",
    "last_name": "Lovelace",
    "email": "ada@example.com",
    "phone": "0600000000",
}


def test_operator_cannot_manage_contacts(client, operator_headers):
    assert client.get("/contacts/", headers=operator_headers).status_code == 403
    assert client.post("/contacts/", json=PAYLOAD, headers=operator_headers).status_code == 403


def test_create_and_list_contacts(client, admin_headers):
    response = client.post("/contacts/", json=PAYLOAD, headers=admin_headers)
    assert response.status_code == 200
    contacts = client.get("/contacts/", headers=admin_headers).json()
    assert contacts[0]["first_name"] == "Ada"


def test_duplicate_email_or_phone_is_a_400_not_a_500(client, admin_headers):
    client.post("/contacts/", json=PAYLOAD, headers=admin_headers)

    same_email = {**PAYLOAD, "phone": "0611111111"}
    assert client.post("/contacts/", json=same_email, headers=admin_headers).status_code == 400

    same_phone = {**PAYLOAD, "email": "autre@example.com"}
    assert client.post("/contacts/", json=same_phone, headers=admin_headers).status_code == 400


def test_contact_needs_email_or_phone(client, admin_headers):
    response = client.post(
        "/contacts/",
        json={"first_name": "Ada", "last_name": "Lovelace"},
        headers=admin_headers,
    )
    assert response.status_code == 422
