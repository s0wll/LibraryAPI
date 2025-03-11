from datetime import date

from fastapi import APIRouter

from src.services.borrows import BorrowsService
from src.api.dependencies import AdminDep, DBDep, UserDep
from src.schemas.borrows import BorrowAddRequest


router = APIRouter(prefix="/borrows", tags=["Выдача книг"])


@router.get("")
async def get_all_borrows(admin_check: AdminDep, db: DBDep):
    return await BorrowsService(db).get_all_borrows()


@router.get("/me")
async def get_my_borrows(db: DBDep, user: UserDep):
    return await BorrowsService(db).get_my_borrows(user.id)


@router.post("")
async def add_borrow(db: DBDep, user: UserDep, borrow_data: BorrowAddRequest):
    borrow = await BorrowsService(db).add_borrow(user, borrow_data)
    return {"status": "OK", "data": borrow}


@router.patch("/return/{borrow_id}")
async def return_book(db: DBDep, user: UserDep, borrow_id: int, return_date: date):
    borrow = await BorrowsService(db).return_book(borrow_id, return_date, user)
    return {"status": "OK", "data": borrow}