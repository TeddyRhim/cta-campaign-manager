HEADER = "first_name,last_name,email,phone,organization\n"


def make_campaign(client, headers):
    return client.post("/campaigns", json={"title": "Import"}, headers=headers).json()["id"]


def upload(client, headers, campaign_id, content, name="contacts.csv"):
    return client.post(
        f"/imports/?campaign_id={campaign_id}",
        files={"file": (name, content, "text/csv")},
        headers=headers,
    )


def test_import_valid_csv(client, operator_headers):
    campaign_id = make_campaign(client, operator_headers)
    csv = HEADER + "Ada,Lovelace,ada@example.com,0600000001,Analytical\n"
    response = upload(client, operator_headers, campaign_id, csv)
    assert response.status_code == 200
    body = response.json()
    assert (body["status"], body["success_count"], body["error_count"]) == ("SUCCESS", 1, 0)

    campaign = client.get(f"/campaigns/{campaign_id}", headers=operator_headers).json()
    assert len(campaign["contacts"]) == 1


def test_import_partial_and_reimport_does_not_duplicate(client, operator_headers):
    campaign_id = make_campaign(client, operator_headers)
    csv = (
        HEADER
        + "Ada,Lovelace,ada@example.com,0600000001,\n"
        + "Sans,Email,pas-un-mail,0600000002,\n"
    )
    body = upload(client, operator_headers, campaign_id, csv).json()
    assert (body["status"], body["success_count"], body["error_count"]) == ("PARTIAL", 1, 1)

    upload(client, operator_headers, campaign_id, csv)
    campaign = client.get(f"/campaigns/{campaign_id}", headers=operator_headers).json()
    assert len(campaign["contacts"]) == 1


def test_import_accepts_french_columns_and_bom(client, operator_headers):
    campaign_id = make_campaign(client, operator_headers)
    csv = "﻿Prénom,Nom,Mail,Téléphone,Société\nAda,Lovelace,ada@example.com,0600000001,X\n"
    response = upload(client, operator_headers, campaign_id, csv.encode("utf-8"))
    assert response.status_code == 200
    assert response.json()["success_count"] == 1


def test_import_rejects_unknown_columns(client, operator_headers):
    campaign_id = make_campaign(client, operator_headers)
    assert upload(client, operator_headers, campaign_id, "a,b\n1,2\n").status_code == 400


def test_import_rejects_non_utf8(client, operator_headers):
    campaign_id = make_campaign(client, operator_headers)
    content = (HEADER + "Zoé,X,z@example.com,0600000003,\n").encode("latin-1")
    assert upload(client, operator_headers, campaign_id, content).status_code == 400


def test_import_into_someone_elses_campaign_is_forbidden(
    client, operator_headers, other_operator_headers
):
    campaign_id = make_campaign(client, operator_headers)
    csv = HEADER + "Ada,Lovelace,ada@example.com,0600000001,\n"
    assert upload(client, other_operator_headers, campaign_id, csv).status_code == 403


def test_import_unknown_campaign(client, operator_headers):
    assert upload(client, operator_headers, 999, HEADER).status_code == 404


def test_dashboard_stats(client, operator_headers):
    campaign_id = make_campaign(client, operator_headers)
    upload(client, operator_headers, campaign_id, HEADER + "Ada,L,a@example.com,0600000001,\n")
    stats = client.get("/dashboard/stats", headers=operator_headers).json()
    assert stats == {"campaigns_count": 1, "contacts_count": 1, "imports_count": 1}
