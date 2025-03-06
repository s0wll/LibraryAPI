from datetime import date

from fastapi import APIRouter, Body, Query

from src.services.authors import AuthorsService
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.authors import AuthorAdd, AuthorPatch


router = APIRouter(prefix="/authors", tags=["Авторы"])


@router.get("")
async def get_authors(
    db: DBDep,
    pagination: PaginationDep,
    name: str | None = Query(None),
    birth_date: date | None = Query(None, example="2000-01-01"),
):
    return await AuthorsService(db).get_filtered_authors(
        pagination,
        name,
        birth_date,
    )


@router.get("/{author_id}")
async def get_author(db: DBDep, author_id: int):
    return await AuthorsService(db).get_author(author_id)


@router.post("")
async def add_author(db: DBDep, author_data: AuthorAdd = Body(embed=True)):
    author = await AuthorsService(db).add_author(author_data)
    return {"status": "OK", "data": author}


@router.put("/{author_id}")
async def edit_author(db: DBDep, author_id: int, author_data: AuthorAdd):
    await AuthorsService(db).edit_author(author_id, author_data)
    return {"status": "OK"}


@router.patch("/{author_id}")
async def partially_edit_author(db: DBDep, author_id: int, author_data: AuthorPatch):
    await AuthorsService(db).partially_edit_author(author_id, author_data)
    return {"status": "OK"}


@router.delete("/{author_id}")
async def delete_author(db: DBDep, author_id: int):
    await AuthorsService(db).delete_author(author_id)
    return {"status": "OK"}