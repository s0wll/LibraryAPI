from datetime import date

from pydantic import BaseModel


class AuthorAdd(BaseModel):
    name: str
    biography: str
    birth_date: date


class Author(AuthorAdd):
    id: int


class AuthorPatch(BaseModel):
    name: str | None = None
    biography: str | None = None
    birth_date: date | None = None
