import logging

from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from pydantic import BaseModel

from src.exceptions import (
    KeyIsStillReferencedException,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
)
from src.CRUD.mappers.base import DataMapper


class BaseCRUD:
    model = None
    mapper: DataMapper = None

    def __init__(self, session) -> None:
        self.session = session

    async def add(self, data: BaseModel) -> BaseModel:
        try:
            add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError as exc:
            logging.error(
                f"Не удалось добавить данные в БД, входные данные={data}, тип ошибки: {type(exc.orig.__cause__)=}"
            )
            if isinstance(exc.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from exc
            else:
                logging.error(
                    f"Незнакомая ошибка, не удалось добавить данные в БД, входные данные={data}, тип ошибки: {type(exc.orig.__cause__)=}"
                )
                raise exc

    async def add_bulk(self, data: list[BaseModel]) -> None:
        try:
            add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
            await self.session.execute(add_data_stmt)
        except IntegrityError as exc:
            logging.error(
                f"Не удалось добавить данные в БД, входные данные={data}, тип ошибки: {type(exc.orig.__cause__)=}"
            )
            if isinstance(exc.orig.__cause__, ForeignKeyViolationError):
                raise ObjectNotFoundException from exc
            else:
                logging.error(
                    f"Незнакомая ошибка, не удалось добавить данные в БД, входные данные={data}, тип ошибки: {type(exc.orig.__cause__)=}"
                )
                raise exc

    async def get_filtered(self, *filter, **filter_by) -> list[BaseModel]:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        models = [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
        if not models:
            logging.error("Ошибка получения данных из БД, данные не найдены")
            raise ObjectNotFoundException
        return models

    async def get_all(self) -> list[BaseModel | None]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by) -> BaseModel | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound as exc:
            logging.error(f"Ошибка получения данных из БД, тип ошибки: {type(exc)=}")
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(
                **data.model_dump(exclude_unset=exclude_unset),
            )
        )
        try:
            await self.session.execute(update_stmt)
        except IntegrityError as exc:
            logging.error(f"Ошибка изменения данных в БД, тип ошибки: {type(exc.orig.__cause__)=}")
            if isinstance(exc.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from exc
            else:
                logging.error(
                    f"Незнакомая ошибка, не удалось удалить данные из БД, тип ошибки: {type(exc.orig.__cause__)=}"
                )
                raise exc

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        try:
            await self.session.execute(delete_stmt)
        except IntegrityError as exc:
            logging.error(f"Ошибка удаления данных из БД, тип ошибки: {type(exc.orig.__cause__)=}")
            if isinstance(exc.orig.__cause__, ForeignKeyViolationError):
                raise KeyIsStillReferencedException from exc
            else:
                logging.error(
                    f"Незнакомая ошибка, не удалось удалить данные из БД, тип ошибки: {type(exc.orig.__cause__)=}"
                )
                raise exc
