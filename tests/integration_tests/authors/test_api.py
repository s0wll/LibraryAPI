import pytest


@pytest.mark.parametrize(
    "name, biography, birth_date, status_code",
    [
        ("test_author", "test_biography", "2025-01-01", 200),
        ("test_author", "test_biography", "2025.01.01", 422),
    ],
)
async def test_authors_api_flow(
    name: str, biography: str, birth_date: str, status_code: int, authentificated_admin_ac
):
    # /get_filtered_authors
    response_get_authors = await authentificated_admin_ac.get("/authors")
    assert response_get_authors.status_code == 200
    if status_code == 200:
        res = response_get_authors.json()
        assert isinstance(res, list)
        assert res

    # /add_author
    response_add_author = await authentificated_admin_ac.post(
        "/authors",
        json={"author_data": {"name": name, "biography": biography, "birth_date": birth_date}},
    )
    assert response_add_author.status_code == status_code
    if response_add_author.status_code == 200:
        new_author = response_add_author.json()
        assert isinstance(new_author, dict)
        assert new_author["data"]["name"] == name
        assert new_author["data"]["biography"] == biography
        assert new_author["data"]["birth_date"] == birth_date
    if status_code != 200:
        return

    # /get_author
    response_get_author = await authentificated_admin_ac.get(f"/authors/{new_author['data']['id']}")
    assert response_get_author.status_code == 200
    if response_add_author.status_code == 200:
        res = response_get_author.json()
        assert isinstance(res, dict)
        assert res["id"] == new_author["data"]["id"]
        assert res["name"] == name
        assert res["biography"] == biography
        assert res["birth_date"] == birth_date
    if status_code != 200:
        return

    # /update_author
    new_birth_date = "2000-01-01"
    response_update_author = await authentificated_admin_ac.put(
        f"/authors/{new_author['data']['id']}",
        json={
            "name": name,
            "biography": biography,
            "birth_date": new_birth_date,
        },
    )
    assert response_update_author.status_code == status_code
    if response_add_author.status_code == 200:
        res = response_update_author.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
    if status_code != 200:
        return

    # /partially_update_author
    new_biography = "updated_biography"
    response_partially_update_author = await authentificated_admin_ac.patch(
        f"/authors/{new_author['data']['id']}",
        json={"biography": new_biography},
    )
    assert response_partially_update_author.status_code == status_code
    if response_add_author.status_code == 200:
        res = response_partially_update_author.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
    if status_code != 200:
        return

    # /delete_author
    response_delete_author = await authentificated_admin_ac.delete(
        f"/authors/{new_author['data']['id']}"
    )
    assert response_delete_author.status_code == status_code
    if response_add_author.status_code == 200:
        res = response_delete_author.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
    if status_code != 200:
        return
