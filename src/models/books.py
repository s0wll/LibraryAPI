from datetime import date
import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.authors import AuthorsOrm


class BooksOrm(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str]
    publication_date: Mapped[date]
    genre: Mapped[str] = mapped_column(String(100))
    quantity: Mapped[int]

    authors: Mapped[list["AuthorsOrm"]] = relationship(
        back_populates="books", secondary="books_authors"
    )


class BooksAuthorsOrm(Base):
    __tablename__ = "books_authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
