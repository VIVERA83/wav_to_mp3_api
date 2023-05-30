import io
from typing import Any

from icecream import ic

from audio.schemes import DownloadLinkSchema, audio_id_query, user_id_query
from audio.utils import UploadFile, convert, create_download_url
from core.components import Request
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.responses import StreamingResponse
from pydantic import UUID4

convertor_route = APIRouter()


@convertor_route.post(
    "/add_audio",
    summary="Добавить звуковой файл",
    description="Добавить звуковой файл в базу данных, обратите внимание `размер файла ограничен`",
    response_description="ссылка на скачивание",
    tags=["AUDIO"],
    response_model=DownloadLinkSchema,
)
async def add_audio(request: "Request", file: UploadFile) -> Any:
    """Добавление звукового файла формата wav в базу данных."""
    audio_id = await request.app.store.audio.add_audio(
        mp3=await convert(file),
        user_id=request.session.get("user_id"),
        file_name=f"{file.filename.split('.')[0]}.mp3",
    )
    return DownloadLinkSchema(url=create_download_url(request, audio_id))


@convertor_route.get(
    "/record",
    summary="Скачать звуковой файл",
    description="Скачать звуковой файил, фаил в формате mp3",
    response_description="звукойвой файил формата mp3",
    tags=["AUDIO"],
    response_model=None,
)
async def get_audio(
        request: "Request", audio_id: UUID4 = audio_id_query, user_id: UUID4 = user_id_query
) -> Any:
    """Скачать mp3 audio."""
    if data := await request.app.store.audio.get_audio(audio_id, user_id):
        headers = {"Content-Disposition": f"attachment; filename={data.file_name}"}
        return StreamingResponse(content=io.BytesIO(data.mp3), media_type="audio/mp3", headers=headers)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Audio recording not found: id={audio_id} user_id={user_id} ",
    )
