from datetime import date

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from src.exceptions import AuthorNotFoundException, AuthorNotFoundHTTPException, BookKeyIsStillReferencedException, BookKeyIsStillReferencedHTTPException, BookNotFoundException, BookNotFoundHTTPException
from src.schemas.books import BookAddRequest, BookPatchRequest
from src.services.books import BooksService
from src.api.dependencies import AdminDep, PaginationDep, DBDep, UserDep


router = APIRouter(prefix="/books", tags=["Книги"])


@router.get("")
@cache(expire=10)
async def get_filtered_books(
    user: UserDep,
    db: DBDep,
    pagination: PaginationDep,
    title: str | None = Query(None),
    publication_date: date | None = Query(None),
    genre: str | None = Query(None),
):
    try:
        return await BooksService(db).get_filtered_books(
            pagination,
            title,
            publication_date,
            genre,
        )
    except BookNotFoundException:
        raise BookNotFoundHTTPException



@router.get("/{book_id}")
@cache(expire=10)
async def get_book(user: UserDep, db: DBDep, book_id: int):
    try:
        return await BooksService(db).get_book(book_id)
    except BookNotFoundException:
        raise BookNotFoundHTTPException

@router.post("")
async def create_book(admin_check: AdminDep, db: DBDep, book_data: BookAddRequest):
    try:
        return await BooksService(db).create_book(book_data)
    except AuthorNotFoundException:
        raise AuthorNotFoundHTTPException


@router.put("/{book_id}")
async def update_book(admin_check: AdminDep, db: DBDep, book_data: BookAddRequest, book_id: int):
    try:
        await BooksService(db).update_book(book_id, book_data)
    except AuthorNotFoundException:
        raise AuthorNotFoundHTTPException
    return {"status": "OK"}


@router.patch("/{book_id}")
async def partially_update_book(admin_check: AdminDep, db: DBDep, book_data: BookPatchRequest, book_id: int):
    await BooksService(db).partially_update_book(book_id, book_data)
    return {"status": "OK"}


@router.delete("/{book_id}")
async def delete_book(admin_check: AdminDep, db: DBDep, book_id: int):
    try:
        await BooksService(db).delete_book(book_id)
    except BookKeyIsStillReferencedException:
        raise BookKeyIsStillReferencedHTTPException
    return {"status": "OK"} 