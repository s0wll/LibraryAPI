from src.CRUD.mappers.mappers import BorrowDataMapper
from src.models.borrows import BorrowsOrm
from src.CRUD.base import BaseCRUD


class BorrowsCRUD(BaseCRUD):
    model = BorrowsOrm
    mapper = BorrowDataMapper
