"""Schemas сервиса Convertor."""

from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID


class AudioSchemaIn(BaseModel):
    user_id: UUID = Field(
        title="Уникальный индификатор пользователя",
        example="a17b2315-5bb8-40d3-8d8a-2d48b6c3144e"
    )
    token: UUID = Field(
        title="token пользователя",
        example="a17b2315-5bb8-40d3-8d8a-2d48b6c3144e"
    )
    audio: bytes = Field(
        title="Аудио фаил в формате wav"
    )


class DownloadLinkSchema(BaseModel):
    url: HttpUrl = Field(title="Ссылка",
                         description="Ссылка на скачивания файла в формате mp3")
