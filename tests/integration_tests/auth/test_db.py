from src.schemas.users import UserAddRequest, UserAdd
from src.services.auth import AuthService

async def test_auth_crud(db):
    # Добавление пользователя
    user_data = UserAddRequest(
        email="test_user@gmail.com",
        username="test_user",
        password="test_user_password"
    )
    hashed_password = AuthService().hash_password(user_data.password)
    new_user_data = UserAdd(email=user_data.email, username=user_data.username, hashed_password=hashed_password)
    new_user = await db.users.add(new_user_data)

    # Получение пользователя и удостоверение, что он есть в БД
    user = await db.users.get_one_or_none(id=new_user.id)
    assert user
    assert user.id == new_user.id
    assert user.email == new_user.email
    assert user.username == new_user.username

    # Получение пользователя с захэшированным паролем
    user_with_hashed_password = await db.users.get_user_with_hashed_password(email=user.email)
    assert user_with_hashed_password
    assert user_with_hashed_password.id == user.id
    assert user_with_hashed_password.email == user.email
    assert user_with_hashed_password.username == user.username
    assert user_with_hashed_password.hashed_password == hashed_password
    
