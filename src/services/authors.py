from datetime import date

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
        return await self.db.authors.get_filtered_authors(
            name=name,
            birth_date=birth_date,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )
    
    async def get_author(self, author_id: int):
        return await self.db.authors.get_one(id=author_id)
    
    async def add_author(self, author_data: AuthorAdd):
        author = await self.db.authors.add(author_data)
        await self.db.commit()
        return author
    
    async def edit_author(self, author_id: int, author_data: AuthorAdd):
        await self.db.authors.edit(id=author_id, data=author_data)
        await self.db.commit()

    async def partially_edit_author(self, author_id: int, author_data: AuthorAdd):
        await self.db.authors.edit(id=author_id, data=author_data, exclude_unset=True)
        await self.db.commit()

    async def delete_author(self, author_id: int):
        await self.db.authors.delete(id=author_id)
        await self.db.commit()
        