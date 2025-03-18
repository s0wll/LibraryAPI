import json
from typing import AsyncGenerator
from unittest import mock

mock.patch(
    "fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f
).start()

from pydantic import BaseModel
import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app
from src.database import Base, engine
from src.models import *  # noqa
from src.config import settings
from src.utils.db_manager import DBManager
from src.database import async_session_maker
from src.schemas.authors import AuthorAdd
from src.schemas.books import BookAdd
from src.schemas.users import UserAdd, UserAddRequest, UserAddToDB
from src.schemas.borrows import BorrowAdd
from src.services.auth import AuthService


@pytest.fixture(scope="session", autouse=True)
def check_test_mode() -> None:
    assert settings.MODE == "TEST"
    assert settings.DB_NAME == "LibraryAPI-test"


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager]:
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def decode_from_json_to_schema(path: str, schema: BaseModel) -> list[BaseModel]:
        with open(path, encoding="utf-8") as json_file:
            data = json.load(json_file)
            return [schema.model_validate(item) for item in data]

    users_data = await decode_from_json_to_schema("tests/mock_users.json", UserAddToDB)
    users_data[0].hashed_password = AuthService().hash_password(password=users_data[0].hashed_password)
    authors_data = await decode_from_json_to_schema("tests/mock_authors.json", AuthorAdd)
    books_data = await decode_from_json_to_schema("tests/mock_books.json", BookAdd)
    borrows_data = await decode_from_json_to_schema("tests/mock_borrows.json", BorrowAdd)

    async with DBManager(session_factory=async_session_maker) as db_:
        await db_.users.add_bulk(users_data)
        await db_.authors.add_bulk(authors_data)
        await db_.books.add_bulk(books_data)
        await db_.borrows.add_bulk(borrows_data)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def add_admin_user(setup_database):
    admin_user = UserAddRequest(
        email="admin@example.com",
        username="admin",
        password="admin_password",
        is_admin=True
    )
    hashed_password = AuthService().hash_password(admin_user.password)
    _admin_user = UserAddToDB(
        email=admin_user.email,
        username=admin_user.username,
        borrowed_books_count=0,
        is_admin=True,
        hashed_password=hashed_password
    )
    async with DBManager(session_factory=async_session_maker) as _db_:
        await _db_.users.add(_admin_user)
        await _db_.commit()


@pytest.fixture(scope="session", autouse=True)
async def authentificated_admin_ac(ac: AsyncClient) -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth/login", json={"email": "admin@example.com", "password": "admin_password"})
        assert response.status_code == 200
        assert ac.cookies["access_token"]
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    response = await ac.post("/auth/register", json={"email": "mark@gmail.com", "username": "mark", "password": "12345"})
    assert response.status_code == 200
    # Решить перенести в юнит тесты или нет


@pytest.fixture(scope="session", autouse=True)
async def authentificated_user_ac(ac, register_user):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth/login", json={"email": "mark@gmail.com", "password": "12345"})
        assert response.status_code == 200
        assert ac.cookies["access_token"]
        yield ac

    