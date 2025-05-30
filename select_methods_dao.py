from dao.dao import UserDAO
from database import connection
from asyncio import run

from schemas import UserPydantic


@connection
async def select_all_users(session):
    return await UserDAO.get_all_users(session)


all_users = run(select_all_users())
for i in all_users:
    user_pydantic = UserPydantic.from_orm(i)
    print(user_pydantic.dict())