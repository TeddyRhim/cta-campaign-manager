HEADER = "first_name,last_name,email,phone,organization\n"


def _campaign(client, headers, title):
    return client.post("/campaigns", json={"title": title}, headers=headers).json()["id"]


def _import(client, headers, campaign_id, lines, name="contacts.csv"):
    return client.post(
        f"/imports/?campaign_id={campaign_id}",
        files={"file": (name, HEADER + "".join(lines), "text/csv")},
        headers=headers,
    )


def test_campaigns_are_paginated_newest_first(client, operator_headers):
    ids = [_campaign(client, operator_headers, f"Campagne {n}") for n in range(5)]

    first = client.get("/campaigns/?page=1&page_size=2", headers=operator_headers).json()
    last = client.get("/campaigns/?page=3&page_size=2", headers=operator_headers).json()

    assert (first["total"], first["page"], first["page_size"]) == (5, 1, 2)
    assert [c["id"] for c in first["items"]] == [ids[4], ids[3]]
    assert [c["id"] for c in last["items"]] == [ids[0]]


def test_a_page_beyond_the_end_is_empty_but_keeps_the_total(client, operator_headers):
    _campaign(client, operator_headers, "Seule")
    body = client.get("/campaigns/?page=9", headers=operator_headers).json()
    assert (body["items"], body["total"]) == ([], 1)


def test_page_bounds_are_validated(client, operator_headers):
    for query in ("page=0", "page_size=0", "page_size=101"):
        assert client.get(f"/campaigns/?{query}", headers=operator_headers).status_code == 422


def test_pagination_keeps_operator_isolation(client, operator_headers, other_operator_headers):
    _campaign(client, operator_headers, "La mienne")
    body = client.get("/campaigns/", headers=other_operator_headers).json()
    assert (body["items"], body["total"]) == ([], 0)


def test_contacts_search_matches_every_word_across_fields(client, admin_headers):
    campaign_id = _campaign(client, admin_headers, "Import")
    _import(
        client,
        admin_headers,
        campaign_id,
        [
            "Ada,Lovelace,ada@example.com,0600000001,\n",
            "Alan,Turing,alan@example.com,0600000002,\n",
            "Grace,Hopper,grace@example.com,0600000003,\n",
        ],
    )

    by_name = client.get("/contacts/?search=ada lovelace", headers=admin_headers).json()
    by_mail = client.get("/contacts/?search=ALAN@", headers=admin_headers).json()
    wildcard = client.get("/contacts/?search=%25", headers=admin_headers).json()

    assert [c["last_name"] for c in by_name["items"]] == ["Lovelace"]
    assert [c["last_name"] for c in by_mail["items"]] == ["Turing"]
    assert wildcard["total"] == 0  # « % » est cherché tel quel, pas comme joker SQL


def test_contacts_are_sorted_by_name(client, admin_headers):
    campaign_id = _campaign(client, admin_headers, "Import")
    _import(
        client,
        admin_headers,
        campaign_id,
        [
            "Grace,Hopper,grace@example.com,0600000003,\n",
            "Ada,Lovelace,ada@example.com,0600000001,\n",
        ],
    )
    body = client.get("/contacts/?page_size=1", headers=admin_headers).json()
    assert (body["total"], body["items"][0]["last_name"]) == (2, "Hopper")


def test_imports_are_paginated_and_searchable(client, operator_headers):
    campaign_id = _campaign(client, operator_headers, "Import")
    line = ["Ada,Lovelace,ada@example.com,0600000001,\n"]
    _import(client, operator_headers, campaign_id, line, name="janvier.csv")
    _import(client, operator_headers, campaign_id, line, name="fevrier.csv")

    page = client.get("/imports/?page_size=1", headers=operator_headers).json()
    found = client.get("/imports/?search=janv", headers=operator_headers).json()

    assert (page["total"], page["items"][0]["filename"]) == (2, "fevrier.csv")
    assert [i["filename"] for i in found["items"]] == ["janvier.csv"]
