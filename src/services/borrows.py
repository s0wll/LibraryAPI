from datetime import date

from fastapi import BackgroundTasks

from src.schemas.users import User
from src.schemas.books import Book
from src.schemas.borrows import Borrow, BorrowAdd, BorrowAddRequest
from src.api.dependencies import UserDep
from src.services.base import BaseService
from src.tasks.tasks import send_borrow_info_email_task
from src.exceptions import BookNotFoundException, BorrowNotFoundException, MaxBooksLimitExceededException, NoBooksAvailableException, ObjectNotFoundException, check_date_to_after_date_from


class BorrowsService(BaseService):
    async def get_all_borrows(self):
        return await self.db.borrows.get_all()

    async def get_my_borrows(self, user_id: int):
        try:
            return await self.db.borrows.get_filtered(user_id=user_id)
        except ObjectNotFoundException:
            raise BorrowNotFoundException
    
    async def add_borrow(self, user: UserDep, borrow_data: BorrowAddRequest, background_tasks: BackgroundTasks):
        check_date_to_after_date_from(borrow_data.date_from, borrow_data.date_to)
        try:
            book_data: Book = await self.db.books.get_one(id=borrow_data.book_id)
        except ObjectNotFoundException:
            raise BookNotFoundException
        _borrow_data = BorrowAdd(user_id=user.id, **borrow_data.model_dump(), is_returned=False)

        if book_data.quantity <= 0:
            raise NoBooksAvailableException
        book_data.quantity -= 1

        if user.borrowed_books_count >= 5:
            raise MaxBooksLimitExceededException
        user.borrowed_books_count += 1

        borrow = await self.db.borrows.add(data=_borrow_data)
        await self.db.books.update(id=book_data.id, data=book_data)
        await self.db.users.update(id=user.id, data=user)
        await self.db.commit()

        background_tasks.add_task(
            send_borrow_info_email_task,
            recipient_email=user.email,
            date_from=borrow_data.date_from,
            date_to=borrow_data.date_to,
            book_id=borrow_data.book_id,
        )

        return borrow
    
    async def return_book(self, borrow_id: int, return_date: date, user: User) -> Borrow:
        borrow_data = await self.db.borrows.get_one(id=borrow_id)
        book_data = await self.db.books.get_one(id=borrow_data.book_id)

        book_data.quantity += 1
        borrow_data.date_to = return_date
        borrow_data.is_returned = True
        user.borrowed_books_count -= 1

        await self.db.books.update(id=book_data.id, data=book_data)
        await self.db.borrows.update(id=borrow_data.id, data=borrow_data)
        await self.db.users.update(id=user.id, data=user)

        await self.db.commit()
        return borrow_data

