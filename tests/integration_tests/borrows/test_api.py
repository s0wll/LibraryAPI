import pytest


async def test_get_all_borrows(authentificated_admin_ac):
    response = await authentificated_admin_ac.get("/borrows")
    assert response.status_code == 200
    if response.status_code == 200:
        borrows = response.json()
        assert isinstance(borrows, list)
        assert len(borrows) > 0
        for borrow in borrows:
            assert isinstance(borrow, dict)
            assert "id" in borrow
            assert "book_id" in borrow
            assert "user_id" in borrow
            assert "date_from" in borrow
            assert "date_to" in borrow
            assert "is_returned" in borrow
    if response.status_code != 200:
        return


@pytest.mark.parametrize(
    "user_id, book_id, date_from, date_to, is_returned, status_code",
    [
        (3, 1, "2025-01-01", "2025-01-02", False, 200),
        (3, 4, "2025-01-01", "2025-01-02", False, 404)
    ]
)
async def test_borrows_api_user_flow(
    user_id: int,
    book_id: int,
    date_from: str,
    date_to: str,
    is_returned: bool,
    status_code: int,
    authentificated_user_ac,
):
    # /add_borrow
    response_add_borrow = await authentificated_user_ac.post(
        "/borrows",
        json={
            "user_id": user_id,
            "book_id": book_id,
            "date_from": date_from,
            "date_to": date_to,
            "is_returned": is_returned,
        }
    )
    assert response_add_borrow.status_code == status_code
    if response_add_borrow.status_code == 200:
        new_borrow = response_add_borrow.json()
        assert isinstance(new_borrow, dict)
        assert new_borrow["data"]["user_id"] == user_id
        assert new_borrow["data"]["book_id"] == book_id
        assert new_borrow["data"]["date_from"] == date_from
        assert new_borrow["data"]["date_to"] == date_to
        assert new_borrow["data"]["is_returned"] == is_returned
    if response_add_borrow.status_code != 200:
        return

    # /get_my_borrows
    response_get_my_borrows = await authentificated_user_ac.get("/borrows/me")
    assert response_get_my_borrows.status_code == 200
    if response_get_my_borrows.status_code == 200:
        borrows = response_get_my_borrows.json()
        assert isinstance(borrows, list)
        assert len(borrows) > 0
    if response_get_my_borrows.status_code != 200:
        return

    # /return_book
    response_return_book = await authentificated_user_ac.patch(
        f"/borrows/return/{new_borrow["data"]["id"]}",
        params={"return_date": "2025-01-02"}
    )
    assert response_return_book.status_code == 200
    if response_return_book.status_code == 200:
        returned_borrow = response_return_book.json()
        assert isinstance(returned_borrow, dict)
        assert returned_borrow["data"]["is_returned"] == True
    if response_return_book.status_code != 200:
        return
    