from src.schemas.books import Book, BookAddRequest, BookAdd, BookAuthorAdd


async def test_books_crud(db):
    # Добавление книги
    book_data = BookAddRequest(
        title="test_db_book",
        description="test_db_book_description",
        publication_date="2025-01-01",
        genre="test_db_book_genre",
        quantity=5,
        authors_ids=[1],
    )
    _book_data = BookAdd(**book_data.model_dump())
    new_book: Book = await db.books.add(_book_data)

    books_authors_data = [
        BookAuthorAdd(book_id=new_book.id, author_id=author_id)
        for author_id in book_data.authors_ids
    ]
    await db.books_authors.add_bulk(books_authors_data)
    await db.commit()

    # Получение этой книги и удостоверение, что она есть
    book = await db.books.get_book_with_rels(id=new_book.id)
    assert book
    assert book.id == new_book.id
    assert book.title == new_book.title
    assert book.description == new_book.description
    assert book.publication_date == new_book.publication_date
    assert book.genre == new_book.genre
    assert book.quantity == new_book.quantity
    assert [book.authors[0].id] == book_data.authors_ids

    # Изменение книги
    updated_book_data = BookAddRequest(
        title="test_db_book_updated",
        description="test_db_book_description_updated",
        publication_date="2025-01-02",
        genre="test_db_book_genre_updated",
        quantity=10,
        authors_ids=[2],
    )
    _updated_book_data = BookAdd(**updated_book_data.model_dump())
    await db.books.update(id=book.id, data=_updated_book_data)
    await db.books_authors.set_book_authors(book.id, authors_ids=updated_book_data.authors_ids)
    await db.commit()
    updated_book = await db.books.get_book_with_rels(id=book.id)
    assert updated_book
    assert updated_book.id == book.id
    assert updated_book.title == updated_book_data.title
    assert updated_book.description == updated_book_data.description
    assert updated_book.publication_date == updated_book_data.publication_date
    assert updated_book.genre == updated_book_data.genre
    assert updated_book.quantity == updated_book_data.quantity
    assert [updated_book.authors[0].id] == updated_book_data.authors_ids

    # Удаление книги
    await db.books_authors.delete(
        book_id=book.id
    )  # Сначала идет удаление элемента с участием данной книги из таблицы m2m
    await db.books.delete(id=book.id)
    await db.commit()
    deleted_book = await db.books.get_one_or_none(id=book.id)
    assert not deleted_book
