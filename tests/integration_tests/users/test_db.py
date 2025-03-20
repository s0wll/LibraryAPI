from src.schemas.users import UserPatch


async def test_users_crud(db):
    # Получение всех пользователей
    users = await db.users.get_all()
    assert users

    # Изменение пользователя
    updated_user_data = UserPatch(email="new_email@example.com", username="new_username")
    await db.users.update(id=users[0].id, data=updated_user_data, exclude_unset=True)
    updated_user = await db.users.get_one_or_none(id=users[0].id)
    assert updated_user.id == users[0].id
    assert updated_user.email == updated_user_data.email
    assert updated_user.username == updated_user_data.username
