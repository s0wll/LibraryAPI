import logging

from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache
from fastapi import BackgroundTasks

from src.exceptions import BookNotFoundException, BookNotFoundHTTPException, BorrowNotFoundException, BorrowNotFoundHTTPException, MaxBooksLimitExceededException, MaxBooksLimitExceededHTTPException, NoBooksAvailableException, NoBooksAvailableHTTPException
from src.services.borrows import BorrowsService
from src.api.dependencies import AdminDep, DBDep, UserDep
from src.schemas.borrows import BorrowAddRequest


router = APIRouter(prefix="/borrows", tags=["Выдача книг"])


@router.get("")
@cache(expire=10)
async def get_all_borrows(admin_check: AdminDep, db: DBDep):
    logging.info("Получение полного списка выдачей книг /get_all_borrows")
    try:
        borrows = await BorrowsService(db).get_all_borrows()
        logging.info("Успешное получение полного списка выдачей книг")
    except BorrowNotFoundException:
        logging.error("Ошибка получения списка выдачей книг: выдачи не найдены")
        raise BorrowNotFoundHTTPException
    return borrows


@router.get("/me")
@cache(expire=10)
async def get_my_borrows(db: DBDep, user: UserDep):
    logging.info("Получение списка выдачей книг текущего пользователя /get_my_borrows")
    try:
        user_borrows = await BorrowsService(db).get_my_borrows(user.id)
        logging.info("Успешное получение списка выдачей книг текущего пользователя")
        return user_borrows
    except BorrowNotFoundException:
        logging.error("Ошибка получения списка выдачей книг текущего пользователя: выдачи не найдены")
        raise BorrowNotFoundHTTPException


@router.post("")
async def add_borrow(db: DBDep, user: UserDep, borrow_data: BorrowAddRequest, background_tasks: BackgroundTasks):
    logging.info("Добавление новой выдачи книги /add_borrow")
    try:
        borrow = await BorrowsService(db).add_borrow(user, borrow_data, background_tasks)
        logging.info("Успешное добавление новой выдачи книги")
    except BookNotFoundException:
        logging.error("Ошибка добавления выдачи: книга не найдена")
        raise BookNotFoundHTTPException
    except NoBooksAvailableException:
        logging.error("Ошибка добавления выдачи: нет доступных книг")
        raise NoBooksAvailableHTTPException
    except MaxBooksLimitExceededException:
        logging.error("Ошибка добавления выдачи: превышен лимит выдачи книг")
        raise MaxBooksLimitExceededHTTPException
    return {"status": "OK", "data": borrow}


@router.patch("/return/{borrow_id}")
async def return_book(db: DBDep, user: UserDep, borrow_id: int, return_date: date):
    logging.info("Возвращение книги /return_book")
    borrow = await BorrowsService(db).return_book(borrow_id, return_date, user)
    logging.info("Успешное возвращение книги")
    return {"status": "OK", "data": borrow}