from datetime import date
import logging

from asyncpg.exceptions import ForeignKeyViolationError
from sqlalchemy import delete, func, insert, select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.exceptions import ObjectNotFoundException
from src.schemas.books import Book
from src.CRUD.base import BaseCRUD
from src.models.books import BooksAuthorsOrm, BooksOrm
from src.CRUD.mappers.mappers import BookAuthorDataMapper, BookDataMapper, BookDataWithRelsMapper


class BooksCRUD(BaseCRUD):
    model = BooksOrm
    mapper = BookDataMapper

    async def get_filtered_books(
        self,
        title: str,
        publication_date: date,
        genre: str,
        limit,
        offset,
    ):
        query = select(self.model).options(selectinload(self.model.authors))
        if title:
            query = query.filter(
                func.lower(self.model.title).contains(title.strip().lower())
            )
        if publication_date:
            query = query.filter(self.model.publication_date == publication_date)
        if genre:
            query = query.filter(
                func.lower(self.model.genre).contains(genre.strip().lower())
            )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        models = [BookDataWithRelsMapper.map_to_domain_entity(book) for book in result.scalars().all()]
        if not models:
            logging.error("Ошибка получения данных книг из БД")
            raise ObjectNotFoundException
        return models

    async def get_book_with_rels(self, **filter_by) -> Book:
        query = select(self.model).options(selectinload(self.model.authors)).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound as exc:
            logging.error("Ошибка получения данных книг и авторов из БД")
            raise ObjectNotFoundException from exc
        return BookDataWithRelsMapper.map_to_domain_entity(model)


class BooksAuthorsCRUD(BaseCRUD):
    model = BooksAuthorsOrm
    mapper = BookAuthorDataMapper

    async def set_book_authors(self, book_id: int, authors_ids: list[str]) -> None:
        get_current_authors_ids_query = select(self.model.author_id).filter_by(book_id=book_id)
        res = await self.session.execute(get_current_authors_ids_query)
        current_authors_ids: list[int] = res.scalars().all()
        ids_to_delete: list[int] = list(set(current_authors_ids))
        ids_to_insert: list[int] = list(set(authors_ids) - set(current_authors_ids))

        if ids_to_delete:
            delete_m2m_authors_stmt = delete(self.model).filter(
                self.model.book_id == book_id,
                self.model.author_id.in_(ids_to_delete),
            )
            await self.session.execute(delete_m2m_authors_stmt)

        if ids_to_insert:
            insert_m2m_authors_stmt = insert(self.model).values(
                [{"book_id": book_id, "author_id": author_id} for author_id in ids_to_insert]
            )
            try:
                await self.session.execute(insert_m2m_authors_stmt)
            except IntegrityError as exc:
                logging.error(f"Ошибка получения данных авторов из БД, тип ошибки: {type(exc.orig.__cause__)=}")
                if isinstance(exc.orig.__cause__, ForeignKeyViolationError):
                    raise ObjectNotFoundException from exc
                else:
                    logging.error(
                        f"Незнакомая ошибка, тип ошибки: {type(exc.orig.__cause__)=}"
                    )
                    raise exc