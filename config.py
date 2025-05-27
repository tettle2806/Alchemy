
# Тут мы создали класс Settings, поместив в него все переменные из файла .env.
# Кроме того, мы описали метод, который позволит генерировать ссылку для асинхронного подключения к базе данных PostgreSQL через SQLAlchemy.

# Далее я назначил переменную settings, как объект класса Settings.
# Теперь у нас появилась возможность обращаться через точку к нужным нам методам и переменным.

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    )

    def get_db_url(self):
        return (f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@'
                f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')


settings = Settings()


print("DB URL =>", settings.get_db_url())
print("DB HOST =>", settings.DB_HOST)