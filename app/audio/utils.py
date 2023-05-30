"""Вспомогательные функции для модуля AUDIO."""
import io
from asyncio import get_event_loop
from concurrent import futures
from typing import Any, Callable, Iterable, Type

from core.components import Request
from core.settings import Settings
from fastapi import File
from pydub import AudioSegment
from starlette.datastructures import UploadFile as StarletteUploadFile


class UploadFile(StarletteUploadFile):
    @classmethod
    def __get_validators__(cls: Type["UploadFile"]) -> Iterable[Callable[..., Any]]:
        yield cls.validate

    @classmethod
    def validate(cls: Type["UploadFile"], file: File) -> Any:
        """Проверка на допустимый размер файла."""
        print(1)
        if not isinstance(file, StarletteUploadFile):
            raise ValueError(f"Expected UploadFile, received: {type(file)}")

        if file.size > Settings().size_wav_file:
            raise ValueError(
                f"Too large file to upload, maximum size 1 Mb: {file.size}"
            )
        return file

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        field_schema.update({"type": "string", "format": "binary"})


def create_download_url(request: "Request", audio_id: str) -> str:
    """Создать ссылку для скачивания файла."""
    return (
        f"http://{request.app.settings.host}:"
        f"{request.app.settings.port}/record?id={audio_id}&user={request.session['user_id']}"
    )


async def convert(file: UploadFile) -> bytes:
    """Конвертирование файла`.wav` в `mp3`.

    Операция по коныертации запускается в отдельном процессе."""
    with futures.ProcessPoolExecutor() as pool:
        return await get_event_loop().run_in_executor(pool, _convert, io.BytesIO(await file.read()))


def _convert(file: io.BytesIO) -> bytes:
    """Конвертирует звуковой фали формата wav в mp3."""
    mp3 = io.BytesIO()
    AudioSegment.from_wav(file).export(mp3, format="mp3")
    return mp3.read()
