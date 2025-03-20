from datetime import date

from fastapi import HTTPException


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=400, detail="Дата взятия книги не может быть позже даты возврата")


# BaseExceptions
class LibraryServiceException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(LibraryServiceException):
    detail = "Объект не найден"


class AuthorNotFoundException(ObjectNotFoundException):
    detail = "Автор не найден"


class BookNotFoundException(ObjectNotFoundException):
    detail = "Книга не найдена"


class UserNotFoundException(ObjectNotFoundException):
    detail = "Пользователь не найден"


class BorrowNotFoundException(LibraryServiceException):
    detail = "Выдача книги не найдена"


class ObjectAlreadyExistsException(LibraryServiceException):
    detail = "Такой объект уже существует"


class UserAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Пользователь уже существует"


class IncorrectPasswordException(LibraryServiceException):
    detail = "Неверный пароль"


class IncorrectTokenException(LibraryServiceException):
    detail = "Некорректный токен"


class KeyIsStillReferencedException(LibraryServiceException):
    detail = "Ключ все еще используется"


class AuthorKeyIsStillReferencedException(LibraryServiceException):
    detail = "Ключ автора все еще используется"


class BookKeyIsStillReferencedException(LibraryServiceException):
    detail = "Ключ книги все еще используется"


class NoBooksAvailableException(LibraryServiceException):
    detail = "Нет доступных книг"


class MaxBooksLimitExceededException(LibraryServiceException):
    detail = "Пользователь не может взять книгу, т.к. у него уже есть максимальное количество книг"


# HTTPExceptions
class LibraryServiceHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class AuthorNotFoundHTTPException(LibraryServiceHTTPException):
    status_code = 404
    detail = "Автор не найден"


class BookNotFoundHTTPException(LibraryServiceHTTPException):
    status_code = 404
    detail = "Книга не найдена"


class BorrowNotFoundHTTPException(LibraryServiceHTTPException):
    status_code = 404
    detail = "Выдача книги не найдена"


class UserEmailNotFoundHTTPException(LibraryServiceHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не найден"


class UserAlreadyExistsHTTPException(LibraryServiceHTTPException):
    status_code = 409
    detail = "Пользователь с таким email/username уже существует"


class IncorrectPasswordHTTPException(LibraryServiceHTTPException):
    status_code = 401
    detail = "Неверный пароль"


class IncorrectTokenHTTPException(LibraryServiceHTTPException):
    status_code = 401
    detail = "Некорректный токен"


class NotAuthenticatedHTTPException(LibraryServiceHTTPException):
    status_code = 401
    detail = "Вы не аутентифицированны/Вы не предоставили токен доступа"


class AuthorKeyIsStillReferencedHTTPException(LibraryServiceHTTPException):
    status_code = 409
    detail = "Ключ таблицы авторов все еще используется в другой таблице"


class BookKeyIsStillReferencedHTTPException(LibraryServiceHTTPException):
    status_code = 409
    detail = "Ключ таблицы книг все еще используется в другой таблице"


class NotAdminHTTPException(LibraryServiceHTTPException):
    status_code = 403
    detail = "У вас недостаточно прав"


class NoBooksAvailableHTTPException(LibraryServiceHTTPException):
    status_code = 404
    detail = "Нет доступных книг"


class MaxBooksLimitExceededHTTPException(LibraryServiceHTTPException):
    status_code = 403
    detail = "Пользователь не может взять книгу, т.к. у него уже есть максимальное количество книг"
