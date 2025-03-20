import logging

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
    logging.info("Получение списка книг /get_filtered_books")
    try:
        books = await BooksService(db).get_filtered_books(
            pagination,
            title,
            publication_date,
            genre,
        )
        logging.info("Успешное получение списка книг")
        return books
    except BookNotFoundException:
        logging.error("Ошибка получения списка книг: книги не найдены")
        raise BookNotFoundHTTPException



@router.get("/{book_id}")
@cache(expire=10)
async def get_book(user: UserDep, db: DBDep, book_id: int):
    logging.info("Получение книги по id /get_book")
    try:
        book = await BooksService(db).get_book(book_id)
        logging.info("Успешное получение книги")
        return book
    except BookNotFoundException:
        logging.error("Ошибка получения книги: книги не найдены")
        raise BookNotFoundHTTPException

@router.post("")
async def create_book(admin_check: AdminDep, db: DBDep, book_data: BookAddRequest):
    logging.info("Создание книги /create_book")
    try:
        book = await BooksService(db).create_book(book_data)
        logging.info("Успешное создание книги")
        return book
    except AuthorNotFoundException:
        logging.error("Ошибка создания книги: автор не найден")
        raise AuthorNotFoundHTTPException


@router.put("/{book_id}")
async def update_book(admin_check: AdminDep, db: DBDep, book_data: BookAddRequest, book_id: int):
    logging.info("Обновление книги по id /update_book")
    try:
        await BooksService(db).update_book(book_id, book_data)
        logging.info("Успешное обновление книги")
    except AuthorNotFoundException:
        logging.error("Ошибка обновления данных книги: автор не найден")
        raise AuthorNotFoundHTTPException
    return {"status": "OK"}


@router.patch("/{book_id}")
async def partially_update_book(admin_check: AdminDep, db: DBDep, book_data: BookPatchRequest, book_id: int):
    logging.info("Частичное обновление книги по id /patch_book")
    try:
        await BooksService(db).partially_update_book(book_id, book_data)
        logging.info("Успешное частичное обновление книги")
    except AuthorNotFoundException:
        logging.error("Ошибка обновления данных книги: автор не найден")
        raise AuthorNotFoundHTTPException
    return {"status": "OK"}


@router.delete("/{book_id}")
async def delete_book(admin_check: AdminDep, db: DBDep, book_id: int):
    logging.info("Удаление книги по id /delete_book")
    try:
        await BooksService(db).delete_book(book_id)
        logging.info("Успешное удаление книги")
    except BookKeyIsStillReferencedException:
        logging.error("Ошибка удаления книги: ключ книги все еще используется")
        raise BookKeyIsStillReferencedHTTPException
    return {"status": "OK"} 