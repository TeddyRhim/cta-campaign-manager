def create_campaign(client, headers, title="Printemps"):
    response = client.post(
        "/campaigns", json={"title": title, "description": "desc"}, headers=headers
    )
    assert response.status_code == 200
    return response.json()


def test_create_and_list_own_campaigns(client, operator_headers, other_operator_headers):
    created = create_campaign(client, operator_headers)
    assert created["status"] == "DRAFT"

    mine = client.get("/campaigns/", headers=operator_headers).json()
    theirs = client.get("/campaigns/", headers=other_operator_headers).json()
    assert [c["id"] for c in mine] == [created["id"]]
    assert theirs == []


def test_admin_sees_all_campaigns(client, operator_headers, admin_headers):
    create_campaign(client, operator_headers)
    assert len(client.get("/campaigns/", headers=admin_headers).json()) == 1


def test_other_operator_cannot_access_campaign(client, operator_headers, other_operator_headers):
    campaign = create_campaign(client, operator_headers)
    url = f"/campaigns/{campaign['id']}"
    assert client.get(url, headers=other_operator_headers).status_code == 403
    assert client.put(url, json={"title": "x"}, headers=other_operator_headers).status_code == 403
    assert client.delete(url, headers=other_operator_headers).status_code == 403


def test_partial_update_keeps_title_and_changes_status(client, operator_headers):
    campaign = create_campaign(client, operator_headers)
    url = f"/campaigns/{campaign['id']}"

    response = client.put(url, json={"status": "ACTIVE"}, headers=operator_headers)
    assert response.status_code == 200
    assert response.json()["status"] == "ACTIVE"
    assert response.json()["title"] == "Printemps"

    response = client.put(url, json={"description": "nouvelle"}, headers=operator_headers)
    assert response.json()["description"] == "nouvelle"
    assert response.json()["status"] == "ACTIVE"


def test_update_with_null_title_is_rejected(client, operator_headers):
    campaign = create_campaign(client, operator_headers)
    response = client.put(
        f"/campaigns/{campaign['id']}", json={"title": None}, headers=operator_headers
    )
    assert response.status_code == 422


def test_update_with_invalid_status_is_rejected(client, operator_headers):
    campaign = create_campaign(client, operator_headers)
    response = client.put(
        f"/campaigns/{campaign['id']}", json={"status": "NOPE"}, headers=operator_headers
    )
    assert response.status_code == 422


def test_delete_campaign(client, operator_headers):
    campaign = create_campaign(client, operator_headers)
    url = f"/campaigns/{campaign['id']}"
    assert client.delete(url, headers=operator_headers).status_code == 200
    assert client.get(url, headers=operator_headers).status_code == 404


def test_link_contact_twice_does_not_duplicate(client, admin_headers):
    campaign = create_campaign(client, admin_headers)
    contact = client.post(
        "/contacts/",
        json={"first_name": "Ada", "last_name": "Lovelace", "email": "ada@example.com"},
        headers=admin_headers,
    ).json()
    url = f"/campaigns/{campaign['id']}/contacts/{contact['id']}"
    client.post(url, headers=admin_headers)
    response = client.post(url, headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()["contacts"]) == 1
