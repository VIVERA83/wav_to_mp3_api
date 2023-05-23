from typing import Any

from convertor.schemes import AudioSchemaIn, DownloadLink
from core.components import Request
from fastapi import APIRouter

convertor_route = APIRouter()


@convertor_route.post(
    "/add_audio",
    summary="Добавить звуковой файл",
    description="Добавить звуковой файл в базу данных",
    response_description="ссылка на скачивание",
    tags=["POST"],
    response_model=DownloadLink,
)
async def add_audio(request: "Request", audio: AudioSchemaIn) -> Any:
    """Добавление звукового файла формата wav в базу данных."""
    return DownloadLink(url="https://github.com/VIVERA83?tab=repositories")
