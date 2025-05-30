from dao.dao import UserDAO
from database import connection
from asyncio import run

from schemas import UserPydantic


@connection
async def select_all_users(session):
    return await UserDAO.get_all_users(session)


@connection
async def select_username_id(session):
    return await UserDAO.get_username_id(session)


@connection
async def select_full_user_info(session, user_id: int):
    rez = await UserDAO.get_user_info(session=session, user_id=user_id)
    if rez:
        return UserPydantic.model_validate(rez).model_dump()
    return {'message': f'Пользователь с ID {user_id} не найден!'}

# info = run(select_full_user_info(user_id=1))
# print(info)
# # {'username': 'yakvenalex', 'email': 'example@example.com', 'profile': None}

# info = run(select_full_user_info(user_id=3))
# print(info)
# {'username': 'john_doe', 'email': 'john.doe@example.com', 'profile': {'first_name': 'John', 'last_name': 'Doe', 'age': 28, 'gender': 'мужчина', 'profession': 'инженер', 'interests': ['hiking', 'photography', 'coding'], 'contacts': {'phone': '+123456789', 'email': 'john.doe@example.com'}}}

# info = run(select_full_user_info(user_id=1113))
# print(info)
# {'message': 'Пользователь с ID 1113 не найден!'}

# rez = run(select_username_id())
# for i in rez:
#     rez = UsernameIdPydantic.from_orm(i)
#     print(rez.dict())

# all_users = run(select_all_users())
# for i in all_users:
#     user_pydantic = UserPydantic.from_orm(i)
#     print(user_pydantic.dict())
