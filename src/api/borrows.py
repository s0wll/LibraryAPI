from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache
from fastapi import BackgroundTasks

from src.exceptions import BookNotFoundException, BookNotFoundHTTPException, BorrowNotFoundException, BorrowNotFoundHTTPException
from src.services.borrows import BorrowsService
from src.api.dependencies import AdminDep, DBDep, UserDep
from src.schemas.borrows import BorrowAddRequest


router = APIRouter(prefix="/borrows", tags=["Выдача книг"])


@router.get("")
@cache(expire=10)
async def get_all_borrows(admin_check: AdminDep, db: DBDep):
    return await BorrowsService(db).get_all_borrows()


@router.get("/me")
@cache(expire=10)
async def get_my_borrows(db: DBDep, user: UserDep):
    try:
        return await BorrowsService(db).get_my_borrows(user.id)
    except BorrowNotFoundException:
        raise BorrowNotFoundHTTPException


@router.post("")
async def add_borrow(db: DBDep, user: UserDep, borrow_data: BorrowAddRequest, background_tasks: BackgroundTasks):
    try:
        borrow = await BorrowsService(db).add_borrow(user, borrow_data, background_tasks)
    except BookNotFoundException:
        raise BookNotFoundHTTPException
    return {"status": "OK", "data": borrow}


@router.patch("/return/{borrow_id}")
async def return_book(db: DBDep, user: UserDep, borrow_id: int, return_date: date):
    borrow = await BorrowsService(db).return_book(borrow_id, return_date, user)
    return {"status": "OK", "data": borrow}