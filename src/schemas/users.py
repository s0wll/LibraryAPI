from pydantic import BaseModel, EmailStr


class UserAddRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserAdd(BaseModel):
    email: EmailStr
    username: str
    hashed_password: str


class User(BaseModel):
    id: int
    email: EmailStr
    username: str


class UserWithHashedPassword(User):
    hashed_password: str