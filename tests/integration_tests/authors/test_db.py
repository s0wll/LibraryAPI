from datetime import date

from src.schemas.authors import AuthorAdd


async def test_author_crud(db):
    # Добавление автора
    author_data = AuthorAdd(
        name="test_db_author",
        biography="test_db_author_biography",
        birth_date=date(year=2025, month=1, day=1),
    )
    new_author = await db.authors.add(author_data)
    await db.commit()

    # Получение этого автора и удостоверение, что он есть
    author = await db.authors.get_one(id=new_author.id)
    assert author
    assert author.id == new_author.id
    assert author.name == new_author.name
    assert author.biography == new_author.biography
    assert author.birth_date == new_author.birth_date

    # Изменение автора
    updated_author_data = AuthorAdd(
        name=author_data.name,
        biography=author_data.biography,
        birth_date=date(year=1799, month=6, day=6),
    )
    await db.authors.update(id=author.id, data=updated_author_data)
    await db.commit()
    updated_author = await db.authors.get_one_or_none(id=new_author.id)
    assert updated_author
    assert updated_author.id == new_author.id
    assert updated_author.birth_date == updated_author_data.birth_date

    # Удаление автора
    await db.authors.delete(id=new_author.id)
    await db.commit()
    deleted_author = await db.authors.get_one_or_none(id=new_author.id)
    assert not deleted_author


