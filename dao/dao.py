from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dao.base import BaseDAO
from models import User, Profile, Post, Comment


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def add_user_with_profile(cls, session: AsyncSession, user_data: dict) -> User:
        """
        Добавляет пользователя и привязанный к нему профиль.

        Аргументы:
        - session: AsyncSession - асинхронная сессия базы данных
        - user_data: dict - словарь с данными пользователя и профиля

        Возвращает:
        - User - объект пользователя
        """
        # Создаем пользователя из переданных данных
        user = cls.model(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        session.add(user)
        await session.flush()  # Чтобы получить user.id для профиля

        # Создаем профиль, привязанный к пользователю
        profile = Profile(
            user_id=user.id,
            first_name=user_data['first_name'],
            last_name=user_data.get('last_name'),
            age=user_data.get('age'),
            gender=user_data['gender'],
            profession=user_data.get('profession'),
            interests=user_data.get('interests'),
            contacts=user_data.get('contacts')
        )
        session.add(profile)

        # Один коммит для обеих операций
        await session.commit()

        return user  # Возвращаем объект пользователя


    @classmethod
    async def get_all_users(cls, session: AsyncSession):
        query = select(cls.model)
        result = await session.execute(query)
        records = result.scalars().all()

        return records

    @classmethod
    async def get_username_id(cls, session:AsyncSession):
        query = select(cls.model.id, cls.model.username)
        print(query)
        result = await session.execute(query)
        records = result.all()
        return records

    @classmethod
    async def get_user_info(cls, session: AsyncSession, user_id: int):
        query = select(cls.model).filter_by(id=user_id)
        result = await session.execute(query)
        user_info =result.scalar_one_or_none()
        return user_info




class ProfileDAO(BaseDAO):
    model = Profile


class PostDAO(BaseDAO):
    model = Post


class CommentDAO(BaseDAO):
    model = Comment