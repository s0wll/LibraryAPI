from datetime import date

from fastapi import APIRouter, Query

from src.schemas.books import BookAddRequest, BookPatchRequest
from src.services.books import BooksService
from src.api.dependencies import AdminDep, PaginationDep, DBDep


router = APIRouter(prefix="/books", tags=["Книги"])


@router.get("")
async def get_filtered_books(
    db: DBDep,
    pagination: PaginationDep,
    title: str | None = Query(None),
    publication_date: date | None = Query(None),
    genre: str | None = Query(None),
):
    return await BooksService(db).get_filtered_books(
        pagination,
        title,
        publication_date,
        genre,
    )



@router.get("/{book_id}")
async def get_book(db: DBDep, book_id: int):
    return await BooksService(db).get_book(book_id)


@router.post("")
async def create_book(admin_check: AdminDep, db: DBDep, book_data: BookAddRequest):
    return await BooksService(db).create_book(book_data)


@router.put("/{book_id}")
async def update_book(admin_check: AdminDep, db: DBDep, book_data: BookAddRequest, book_id: int):
    await BooksService(db).update_book(book_id, book_data)
    return {"status": "OK"}


@router.patch("/{book_id}")
async def partially_update_book(admin_check: AdminDep, db: DBDep, book_data: BookPatchRequest, book_id: int):
    await BooksService(db).partially_update_book(book_id, book_data)
    return {"status": "OK"}


@router.delete("/{book_id}")
async def delete_book(admin_check: AdminDep, db: DBDep, book_id: int):
    await BooksService(db).delete_book(book_id)
    return {"status": "OK"} 