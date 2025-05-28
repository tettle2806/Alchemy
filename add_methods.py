from sqlalchemy.ext.asyncio import AsyncSession
from database import connection
from asyncio import run
from models import User, Profile
from sql_enums import GenderEnum, ProfessionEnum


@connection
async def create_user_example_1(username: str, email: str, password: str, session: AsyncSession) -> int:
    """
    Создает нового пользователя с использованием ORM SQLAlchemy.

    Аргументы:
    - username: str - имя пользователя
    - email: str - адрес электронной почты
    - password: str - пароль пользователя
    - session: AsyncSession - асинхронная сессия базы данных

    Возвращает:
    - int - идентификатор созданного пользователя
    """

    user = User(username=username, email=email, password=password)
    session.add(user)
    await session.commit()
    return user.id


@connection
async def get_user_by_id_example_2(username: str, email: str, password: str,
                                   first_name: str,
                                   last_name: str | None,
                                   age: str | None,
                                   gender: GenderEnum,
                                   profession: ProfessionEnum | None,
                                   interests: list | None,
                                   contacts: dict | None,
                                   session: AsyncSession) -> dict[str, int]:
    user = User(
        username=username,
        email=email,
        password=password,
    )
    session.add(user)
    await session.commit()

    profile = Profile(
        user_id=user.id,
        first_name=first_name,
        last_name=last_name,
        age=age,
        gender=gender,
        profession=profession,
        interests=interests,
        contacts=contacts
    )

    session.add(profile)
    await session.commit()
    print(f'Создан пользователь с ID {user.id} и ему присвоен профиль с ID {profile.id}')
    return {'user_id': user.id, 'profile_id': profile.id}


@connection
async def get_user_by_id_example_3(username: str, email: str, password: str,
                                   first_name: str,
                                   last_name: str | None,
                                   age: str | None,
                                   gender: GenderEnum,
                                   profession: ProfessionEnum | None,
                                   interests: list | None,
                                   contacts: dict | None,
                                   session: AsyncSession) -> dict[str, int]:
    try:
        user = User(username=username, email=email, password=password)
        session.add(user)
        await session.flush()  # Промежуточный шаг для получения user.id без коммита

        profile = Profile(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            profession=profession,
            interests=interests,
            contacts=contacts
        )
        session.add(profile)

        # Один коммит для обоих действий
        await session.commit()

        print(f'Создан пользователь с ID {user.id} и ему присвоен профиль с ID {profile.id}')
        return {'user_id': user.id, 'profile_id': profile.id}

    except Exception as e:
        await session.rollback()  # Откатываем транзакцию при ошибке
        raise e


@connection
async def create_user_example_4(user_data: list[dict], session: AsyncSession) -> list[int]:
    """
    Создает нескольких пользователей с использованием ORM SQLAlchemy.

    Аргументы:
    - users_data: list[dict] - список словарей, содержащих данные пользователей
      Каждый словарь должен содержать ключи: 'username', 'email', 'password'.
    - session: AsyncSession - асинхронная сессия базы данных

    Возвращает:
    - list[int] - список идентификаторов созданных пользователей
    """

    user_list = [
        User(username=user['username'],
             email=user['email'],
             password=user['password']
             )
        for user in user_data
    ]

    session.add_all(user_list)
    await session.commit()
    return [user.id for user in user_list]



# user_profile = run(get_user_by_id_example_2(
#     username="john_doe",
#     email="john.doe@example.com",
#     password="password123",
#     first_name="John",
#     last_name="Doe",
#     age=28,
#     gender=GenderEnum.MALE,
#     profession=ProfessionEnum.ENGINEER,
#     interests=["hiking", "photography", "coding"],
#     contacts={"phone": "+123456789", "email": "john.doe@example.com"},
# ))

# user_profile_2 = run(get_user_by_id_example_3(
#     username="john",
#     email="doe@example.com",
#     password="pass23",
#     first_name="Jon",
#     last_name="Do",
#     age=23,
#     gender=GenderEnum.MALE,
#     profession=ProfessionEnum.DEVELOPER,
#     interests=["hiking", "photography", "coding"],
#     contacts={"phone": "+123456789", "email": "john.doe@example.com"},
# ))
