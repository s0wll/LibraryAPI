from datetime import date

from src.exceptions import AuthorNotFoundException, BookKeyIsStillReferencedException, BookNotFoundException, KeyIsStillReferencedException, ObjectNotFoundException
from src.schemas.books import Book, BookAdd, BookAddRequest, BookAuthorAdd, BookPatch, BookPatchRequest
from src.services.base import BaseService


class BooksService(BaseService):
    async def get_filtered_books(
        self,
        pagination,
        title,
        publication_date: date | None,
        genre: str | None,
    ):
        per_page = pagination.per_page or 5
        try:
            return await self.db.books.get_filtered_books(
                title=title,
                publication_date=publication_date,
                genre=genre,
                limit=per_page,
                offset=per_page * (pagination.page - 1),
            )
        except ObjectNotFoundException:
            raise BookNotFoundException

    async def get_book(self, book_id: int):
        try:
            return await self.db.books.get_book_with_rels(id=book_id)
        except ObjectNotFoundException:
            raise BookNotFoundException

    async def create_book(
        self,
        book_data: BookAddRequest,
    ):
        _book_data = BookAdd(**book_data.model_dump())
        book: Book = await self.db.books.add(_book_data)

        books_authors_data = [
            BookAuthorAdd(book_id=book.id, author_id=author_id) for author_id in book_data.authors_ids
        ]
        if books_authors_data:
            try:
                await self.db.books_authors.add_bulk(books_authors_data)
            except ObjectNotFoundException:
                raise AuthorNotFoundException                
        await self.db.commit()
        return book
    
    async def update_book(self, book_id: int, book_data: BookAddRequest):
        _book_data = BookAdd(**book_data.model_dump())
        await self.db.books.update(id=book_id, data=_book_data)
        try:
            await self.db.books_authors.set_book_authors(
                book_id, authors_ids=book_data.authors_ids
            )
        except ObjectNotFoundException:
                raise AuthorNotFoundException      
        await self.db.commit()

    async def partially_update_book(self, book_id: int, book_data: BookPatchRequest):
        _book_data_dict = book_data.model_dump(exclude_unset=True)
        _book_data = BookPatch(**_book_data_dict)
        await self.db.books.update(id=book_id, data=_book_data, exclude_unset=True)
        if "authors_ids" in _book_data_dict:
            try:
                await self.db.books_authors.set_book_authors(
                    book_id, authors_ids=_book_data_dict["authors_ids"]
                )
            except ObjectNotFoundException:
                raise AuthorNotFoundException
        await self.db.commit()

    async def delete_book(self, book_id: int):
        try:
            await self.db.books.delete(id=book_id)
            await self.db.commit()
        except KeyIsStillReferencedException:
            raise BookKeyIsStillReferencedException

