from typing import Any
from uuid import UUID

from icecream import ic

from audio.schemes import AudioSchemaIn, DownloadLinkSchema
from core.components import Request
from fastapi import APIRouter, File, UploadFile

convertor_route = APIRouter()


@convertor_route.post(
    "/add_audio",
    summary="Добавить звуковой файл",
    description="Добавить звуковой файл в базу данных",
    response_description="ссылка на скачивание",
    tags=["POST"],
    response_model=DownloadLinkSchema,
)
async def add_audio(request: "Request", audio: AudioSchemaIn) -> Any:
    # async def add_audio(request: "Request", user_id: UUID, audio: UploadFile) -> Any:
    """Добавление звукового файла формата wav в базу данных."""
    audio_id = await request.app.store.audio.add_audio(
        mp3=b"audio", user_id=audio.user_id, file_name="Hello")
    ic(audio_id)
    return DownloadLinkSchema(url="https://github.com/VIVERA83?tab=repositories")


@convertor_route.get(
    "/record",
    summary="Скачать звуковой файл",
    description="Скачать звуковой файил, фаил в формате mp3",
    response_description="фаёл mp3",
    tags=["GET"],
)
async def get_audio(request: "Request", id: UUID, user: UUID):
    """Скачать mp3 audio."""
    result = await request.app.store.audio.get_audio(id, user)
    return result
    # http: // host: port / record?id = id_записи & user = id_пользователя.
