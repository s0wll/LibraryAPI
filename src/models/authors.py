from datetime import date
import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.books import BooksOrm


class AuthorsOrm(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    biography: Mapped[str]
    birth_date: Mapped[date]

    books: Mapped[list["BooksOrm"]] = relationship(
        back_populates="authors", secondary="books_authors"
    )
