from datetime import datetime

from sqlalchemy import func, Integer, ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.testing.schema import mapped_column

from typing import Annotated, List
from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from config import settings

DATABASE_URL = settings.get_db_url()

# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(url=DATABASE_URL)
# Создаем фабрику сессий для взаимодействия с базой данных
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

uniq_str_an = Annotated[str, mapped_column(unique=True)] # Аннотация для уникальных строковых полей
array_or_none_an = Annotated[List[str] | None, mapped_column(ARRAY(String))] # Аннотация для массивов строк или None

# Базовый класс для всех моделей
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True  # Класс абстрактный, чтобы не создавать отдельную таблицу для него

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

# Описание конфигурации
#
#     DeclarativeBase: Основной класс для всех моделей, от которого будут наследоваться все таблицы (модели таблиц). Эту особенность класса мы будем использовать неоднократно.
#
#     AsyncAttrs: Позволяет создавать асинхронные модели, что улучшает производительность при работе с асинхронными операциями.
#
#     create_async_engine: Функция, создающая асинхронный движок для соединения с базой данных по предоставленному URL.
#
#     async_sessionmaker: Фабрика сессий для асинхронного взаимодействия с базой данных. Сессии используются для выполнения запросов и транзакций.
