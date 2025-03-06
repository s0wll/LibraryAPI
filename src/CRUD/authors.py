from datetime import date

from sqlalchemy import select, func

from src.schemas.authors import Author
from src.CRUD.base import BaseCRUD
from src.models.authors import AuthorsOrm
from src.CRUD.mappers.mappers import AuthorDataMapper


class AuthorsCRUD(BaseCRUD):
    model = AuthorsOrm
    mapper = AuthorDataMapper

    async def get_filtered_authors(
        self,
        name: str,
        birth_date: date,
        limit,
        offset,
    ) -> list[Author]:
        query = select(AuthorsOrm)
        if name:
            query = query.filter(
                func.lower(AuthorsOrm.name).contains(name.strip().lower())
            )
        if birth_date:
            query = query.filter(AuthorsOrm.birth_date == birth_date)
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(author) for author in result.scalars().all()]
