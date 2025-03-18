import pytest


@pytest.mark.parametrize(
    "title, description, publication_date, genre, quantity, authors_ids, status_code",
    [
        (
            "test_api_book1", 
            "test_api_book1_description",
            "2025-01-01",
            "test_api_book1_genre",
            1,
            [1],
            200,
        ),
        (
            "test_api_book2", 
            "test_api_book2_description",
            "2025.10.10",
            "test_api_book2_genre",
            2,
            [2],
            422,
        )
    ]
)
async def test_books_api_flow(
    title: str,
    description: str,
    publication_date: str,
    genre: str,
    quantity: int,
    authors_ids: list[int],
    status_code: int,
    authentificated_admin_ac,
):
    # /get_filtered_books
    response_get_books = await authentificated_admin_ac.get("/books")
    assert response_get_books.status_code == 200
    if response_get_books.status_code == 200:
        res = response_get_books.json()
        assert isinstance(res, list)
        assert res

    # /add_book
    response_add_book = await authentificated_admin_ac.post(
        "/books",
        json={
            "title": title,
            "description": description,
            "publication_date": publication_date,
            "genre": genre,
            "quantity": quantity,
            "authors_ids": authors_ids,
        }
    )
    assert response_add_book.status_code == status_code
    if response_add_book.status_code == 200:
        new_book = response_add_book.json()
        assert isinstance(new_book, dict)
        assert new_book["title"] == title
        assert new_book["description"] == description
        assert new_book["publication_date"] == publication_date
        assert new_book["genre"] == genre
        assert new_book["quantity"] == quantity
    if status_code != 200:
        return
    
    # /get_book
    response_get_book = await authentificated_admin_ac.get(f"/books/{new_book["id"]}")
    assert response_get_book.status_code == status_code
    if response_get_book.status_code == 200:
        res = response_get_book.json()
        assert isinstance(res, dict)
        assert res["title"] == title
        assert res["description"] == description
        assert res["publication_date"] == publication_date
        assert res["genre"] == genre
        assert res["quantity"] == quantity
    if status_code != 200:
        return
    
    # /update_book
    updated_quantity = 3
    response_update_book = await authentificated_admin_ac.put(
        f"/books/{new_book["id"]}",
        json={
            "title": title,
            "description": description,
            "publication_date": publication_date,
            "genre": genre,
            "quantity": updated_quantity,
            "authors_ids": authors_ids,
        }
    )
    assert response_update_book.status_code == status_code
    if response_update_book.status_code == 200:
        res = response_update_book.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
    if status_code != 200:
        return
    
    # /partially_update_book
    new_genre = "updated_genre"
    response_partially_update_book = await authentificated_admin_ac.patch(
        f"/books/{new_book["id"]}",
        json={
            "genre": new_genre,
        }
    )
    assert response_partially_update_book.status_code == status_code
    if response_partially_update_book.status_code == 200:
        res = response_partially_update_book.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
    if status_code != 200:
        return
    
    # /delete_book
    response_delete_book = await authentificated_admin_ac.delete(f"/books/{new_book["id"]}")
    assert response_delete_book.status_code == status_code
    if status_code == 200:
        res = response_delete_book.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
    if status_code != 200:
        return
    