from datetime import date

from src.exceptions import (
    AuthorKeyIsStillReferencedException,
    AuthorNotFoundException,
    KeyIsStillReferencedException,
    ObjectNotFoundException,
)
from src.schemas.authors import AuthorAdd
from src.services.base import BaseService


class AuthorsService(BaseService):
    async def get_filtered_authors(
        self,
        pagination,
        name: str | None,
        birth_date: date | None,
        # Добавить фильтрацию по книгам
    ):
        per_page = pagination.per_page or 5
        try:
            return await self.db.authors.get_filtered_authors(
                name=name,
                birth_date=birth_date,
                limit=per_page,
                offset=per_page * (pagination.page - 1),
            )
        except ObjectNotFoundException:
            raise AuthorNotFoundException

    async def get_author(self, author_id: int):
        try:
            return await self.db.authors.get_one(id=author_id)
        except ObjectNotFoundException:
            raise AuthorNotFoundException

    async def add_author(self, author_data: AuthorAdd):
        author = await self.db.authors.add(author_data)
        await self.db.commit()
        return author

    async def update_author(self, author_id: int, author_data: AuthorAdd):
        await self.db.authors.update(id=author_id, data=author_data)
        await self.db.commit()

    async def partially_update_author(self, author_id: int, author_data: AuthorAdd):
        await self.db.authors.update(id=author_id, data=author_data, exclude_unset=True)
        await self.db.commit()

    async def delete_author(self, author_id: int):
        try:
            await self.db.authors.delete(id=author_id)
            await self.db.commit()
        except KeyIsStillReferencedException:
            raise AuthorKeyIsStillReferencedException
