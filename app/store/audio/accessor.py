from uuid import UUID

from audio.models import Mp3Model
from base.base_accessor import BaseAccessor
from sqlalchemy import insert, select


class AudioAccessor(BaseAccessor):
    async def add_audio(self, mp3: bytes, file_name: str, user_id) -> UUID:
        """Добавление новой аудио записи."""
        async with self.app.database.session.begin().session as session:
            smtp = insert(Mp3Model).values(
                mp3=mp3,
                file_name=file_name,
                user_id=user_id,
            ).returning(Mp3Model.id)
            result = await session.execute(smtp)
            await session.commit()
            return result.fetchone()[0]

    async def get_audio(self, id: UUID, user_id: UUID) -> Mp3Model:
        """Получить аудио запись."""
        async with self.app.database.session.begin().session as session:
            smtp = select(Mp3Model).where(Mp3Model.id == id, Mp3Model.user_id == user_id)
            result = await session.execute(smtp)
            return result.first()[0]
