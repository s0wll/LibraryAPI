import logging

from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.exceptions import AuthorKeyIsStillReferencedException, AuthorKeyIsStillReferencedHTTPException, AuthorNotFoundException, AuthorNotFoundHTTPException
from src.services.authors import AuthorsService
from src.api.dependencies import AdminDep, PaginationDep, DBDep
from src.schemas.authors import AuthorAdd, AuthorPatch


router = APIRouter(prefix="/authors", tags=["Авторы"])


@router.get("")
@cache(expire=10)
async def get_filtered_authors(
    admin_check: AdminDep,
    db: DBDep,
    pagination: PaginationDep,
    name: str | None = Query(None),
    birth_date: date | None = Query(None, example="2000-01-01"),
):
    logging.info("Получение списка авторов /get_filtered_authors")
    try:
        authors = await AuthorsService(db).get_filtered_authors(
            pagination,
            name,
            birth_date,)
        logging.info("Успешное получение списка авторов")
        return authors
    except AuthorNotFoundException:
        logging.error("Ошибка получения списка авторов: авторы не найден")
        raise AuthorNotFoundHTTPException


@router.get("/{author_id}")
@cache(expire=10)
async def get_author(admin_check: AdminDep, db: DBDep, author_id: int):
    logging.info("Получение информации о конкретном авторе /get_author")
    try:
        author = await AuthorsService(db).get_author(author_id)
        logging.info("Успешное получение информации о конкретном авторе")
        return author
    except AuthorNotFoundException:
        logging.error("Ошибка получения информации о конкретном авторе: автор не найден")
        raise AuthorNotFoundHTTPException


@router.post("")
async def add_author(admin_check: AdminDep, db: DBDep, author_data: AuthorAdd = Body(embed=True)):
    logging.info("Добавление автора /add_author")
    author = await AuthorsService(db).add_author(author_data)
    logging.info("Успешное добавление автора")
    return {"status": "OK", "data": author}


@router.put("/{author_id}")
async def update_author(admin_check: AdminDep, db: DBDep, author_id: int, author_data: AuthorAdd):
    logging.info("Обновление данных об авторе /update_author")
    await AuthorsService(db).update_author(author_id, author_data)
    logging.info("Успешное обновление данных об авторе")
    return {"status": "OK"}


@router.patch("/{author_id}")
async def partially_update_author(admin_check: AdminDep, db: DBDep, author_id: int, author_data: AuthorPatch):
    logging.info("Частичное обновление данных об авторе /partially_update_author")
    await AuthorsService(db).partially_update_author(author_id, author_data)
    logging.info("Успешное частичное обновление данных об авторе")
    return {"status": "OK"}


@router.delete("/{author_id}")
async def delete_author(admin_check: AdminDep, db: DBDep, author_id: int):
    logging.info("Удаление автора /delete_author")
    try:
        await AuthorsService(db).delete_author(author_id)
        logging.info("Успешное удаление автора")
    except AuthorKeyIsStillReferencedException:
        logging.error("Ошибка удаления автора: ключ автора все еще используется")
        raise AuthorKeyIsStillReferencedHTTPException
    return {"status": "OK"}