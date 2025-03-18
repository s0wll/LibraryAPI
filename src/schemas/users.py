from pydantic import BaseModel, EmailStr


class UserAddRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserAdd(BaseModel):
    email: EmailStr
    username: str
    hashed_password: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserPatch(BaseModel):
    email: EmailStr | None
    username: str | None


class User(BaseModel):
    id: int
    email: EmailStr
    username: str
    borrowed_books_count: int
    is_admin: bool


class UserWithHashedPassword(User):
    hashed_password: str


class UserAddToDB(BaseModel):
    email: EmailStr
    username: str
    borrowed_books_count: int
    is_admin: bool
    hashed_password: str


class UserIsAdminRequest(BaseModel):
    is_admin: bool = False