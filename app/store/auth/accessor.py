from uuid import UUID

from auth.models import UserModel
from base.base_accessor import BaseAccessor
from sqlalchemy import insert, select
from icecream import ic

class AuthAccessor(BaseAccessor):
    async def create_user(self, user_name: str, email: str, password: str) -> UserModel:
        """Добавление нового поьзователя в БД"""
        ic(self.app.settings.postgres.dsn)
        async with self.app.database.session.begin().session as session:
            smtp = (
                insert(UserModel)
                .values(
                    user_name=user_name,
                    email=email,
                    password=password,
                )
                .returning(UserModel)
            )
            user = await session.execute(smtp)
            await session.commit()
            return user.fetchone()[0]

    async def get_user_by_token(self, token: UUID) -> UserModel:
        """Получить пользователя по token."""
        async with self.app.database.session.begin().session as session:
            smtp = select(UserModel).where(UserModel.token == token)
            if user := (await session.execute(smtp)).fetchone():
                return user[0]

    async def get_user_by_email(self, email: str) -> UserModel:
        """Получить пользователя по email."""
        async with self.app.database.session.begin().session as session:
            smtp = select(UserModel).where(UserModel.email == email)
            if user := (await session.execute(smtp)).fetchone():
                return user[0]
