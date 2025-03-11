from datetime import date

from src.schemas.users import User
from src.schemas.books import Book
from src.schemas.borrows import Borrow, BorrowAdd, BorrowAddRequest
from src.api.dependencies import UserDep
from src.services.base import BaseService


class BorrowsService(BaseService):
    async def get_all_borrows(self):
        return await self.db.borrows.get_all()

    async def get_my_borrows(self, user_id: int):
        return await self.db.borrows.get_filtered(user_id=user_id)
    
    async def add_borrow(self, user: UserDep, borrow_data: BorrowAddRequest):
        # Реализовать проверку даты
        book_data: Book = await self.db.books.get_one(id=borrow_data.book_id)
        _borrow_data = BorrowAdd(user_id=user.id, **borrow_data.model_dump(), is_returned=False)

        if book_data.quantity <= 0:
            raise Exception("Таких книг не осталось")
        book_data.quantity -= 1

        if user.borrowed_books_count >= 5:
            raise Exception("Вы уже взяли 5 книг")
        user.borrowed_books_count += 1

        borrow = await self.db.borrows.add(data=_borrow_data)
        await self.db.books.update(id=book_data.id, data=book_data)
        await self.db.users.update(id=user.id, data=user)
        await self.db.commit()
        return borrow
    
    async def return_book(self, borrow_id: int, return_date: date, user: User) -> Borrow:
        borrow_data = await self.db.borrows.get_one(id=borrow_id)
        book_data = await self.db.books.get_one(id=borrow_data.book_id)

        book_data.quantity
        borrow_data.date_to = return_date
        borrow_data.is_returned = True
        user.borrowed_books_count -= 1

        await self.db.books.update(id=book_data.id, data=book_data)
        await self.db.borrows.update(id=borrow_data.id, data=borrow_data)
        await self.db.users.update(id=user.id, data=user)

        await self.db.commit()
        return borrow_data

