from auth.models import UserModel
from base.base_accessor import BaseAccessor
from sqlalchemy import insert


class AuthAccessor(BaseAccessor):
    async def create_user(self, user_name: str, email: str) -> UserModel:
        """Добавление нового поьзователя в БД"""
        async with self.app.database.session.begin().session as session:
            smtp = (
                insert(UserModel)
                .values(
                    user_name=user_name,
                    email=email,
                )
                .returning(UserModel)
            )
            user = await session.execute(smtp)
            await session.commit()
            return user.fetchone()[0]
