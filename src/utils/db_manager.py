from src.CRUD.borrows import BorrowsCRUD
from src.CRUD.authors import AuthorsCRUD
from src.CRUD.books import BooksAuthorsCRUD, BooksCRUD
from src.CRUD.users import UsersCRUD


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.authors = AuthorsCRUD(self.session)
        self.books = BooksCRUD(self.session)
        self.books_authors = BooksAuthorsCRUD(self.session)
        self.users = UsersCRUD(self.session)
        self.borrows = BorrowsCRUD(self.session)

        return self
    
    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()