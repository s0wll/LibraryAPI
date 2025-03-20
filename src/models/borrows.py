from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from src.database import Base


class BorrowsOrm(Base):
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    is_returned: Mapped[bool] = mapped_column(default=True)
