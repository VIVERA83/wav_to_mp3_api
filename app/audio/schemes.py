"""Schemas сервиса Convertor."""
from fastapi import Query
from pydantic import UUID4, BaseModel, Field, HttpUrl

user_id_query: UUID4 = Query(
    title="Уникальный индификатор пользователя",
    example="a17b2315-5bb8-40d3-8d8a-2d48b6c3144e",
    alias="user",
)
audio_id_query: UUID4 = Query(
    title="Уникальный индификатор аудиозаписи",
    example="a17b2315-5bb8-40d3-8d8a-2d48b6c3144e",
    alias="id",
)


class DownloadLinkSchema(BaseModel):
    url: HttpUrl = Field(
        title="Ссылка", description="Ссылка на скачивания файла в формате mp3"
    )
