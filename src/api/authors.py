from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.exceptions import AuthorAlreadyExistsException, AuthorAlreadyExistsHTTPException, AuthorKeyIsStillReferencedException, AuthorKeyIsStillReferencedHTTPException, AuthorNotFoundException, AuthorNotFoundHTTPException
from src.services.authors import AuthorsService
from src.api.dependencies import AdminDep, PaginationDep, DBDep
from src.schemas.authors import AuthorAdd, AuthorPatch


router = APIRouter(prefix="/authors", tags=["Авторы"])


@router.get("")
@cache(expire=10)
async def get_authors(
    admin_check: AdminDep,
    db: DBDep,
    pagination: PaginationDep,
    name: str | None = Query(None),
    birth_date: date | None = Query(None, example="2000-01-01"),
):
    try:
        return await AuthorsService(db).get_filtered_authors(
            pagination,
            name,
            birth_date,
        )
    except AuthorNotFoundException:
        raise AuthorNotFoundHTTPException


@router.get("/{author_id}")
@cache(expire=10)
async def get_author(admin_check: AdminDep, db: DBDep, author_id: int):
    try:
        return await AuthorsService(db).get_author(author_id)
    except AuthorNotFoundException:
        raise AuthorNotFoundHTTPException


@router.post("")
async def add_author(admin_check: AdminDep, db: DBDep, author_data: AuthorAdd = Body(embed=True)):
    try:
        author = await AuthorsService(db).add_author(author_data)
    except AuthorAlreadyExistsException:
        raise AuthorAlreadyExistsHTTPException
    return {"status": "OK", "data": author}


@router.put("/{author_id}")
async def update_author(admin_check: AdminDep, db: DBDep, author_id: int, author_data: AuthorAdd):
    await AuthorsService(db).update_author(author_id, author_data)
    return {"status": "OK"}


@router.patch("/{author_id}")
async def partially_update_author(admin_check: AdminDep, db: DBDep, author_id: int, author_data: AuthorPatch):
    await AuthorsService(db).partially_update_author(author_id, author_data)
    return {"status": "OK"}


@router.delete("/{author_id}")
async def delete_author(admin_check: AdminDep, db: DBDep, author_id: int):
    try:
        await AuthorsService(db).delete_author(author_id)
    except AuthorKeyIsStillReferencedException:
            raise AuthorKeyIsStillReferencedHTTPException
    return {"status": "OK"}