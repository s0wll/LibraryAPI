from src.schemas.borrows import Borrow, BorrowAdd, BorrowAddRequest


async def test_borrows_crud(db):
    # Добавление выдачи книги
    borrow_data = BorrowAddRequest(
        book_id=1,
        date_from="2025-01-01",
        date_to="2025-01-02",
    )
    _borrow_data = BorrowAdd(user_id=1, is_returned=False, **borrow_data.model_dump())
    new_borrow: Borrow = await db.borrows.add(_borrow_data)
    await db.commit()

    # Получение этой книги и удостоверение, что она есть
    borrow = await db.borrows.get_one(id=new_borrow.id)
    assert borrow
    assert borrow.id == new_borrow.id
    assert borrow.user_id == new_borrow.user_id
    assert borrow.book_id == new_borrow.book_id
    assert borrow.date_from == new_borrow.date_from
    assert borrow.date_to == new_borrow.date_to
