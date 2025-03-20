from datetime import date

from pydantic import BaseModel


class BorrowAddRequest(BaseModel):
    book_id: int
    date_from: date
    date_to: date


class BorrowAdd(BaseModel):
    user_id: int
    book_id: int
    date_from: date
    date_to: date
    is_returned: bool


class Borrow(BorrowAdd):
    id: int
