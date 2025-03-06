from pydantic import BaseModel


class AuthorAdd(BaseModel):
    name: str
    biography: str
    birth_date: str


class Author(AuthorAdd):
    id: int