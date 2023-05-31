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
import filetype


class UploadFile(StarletteUploadFile):
    @classmethod
    def __get_validators__(cls: Type["UploadFile"]) -> Iterable[Callable[..., Any]]:
        yield cls.validate

    @classmethod
    def validate(cls: Type["UploadFile"], file: File) -> Any:
        """Проверка файла.

        1. Проверка типа переменной file.
        2. Проверка на допустимый размер файла Settings().size_wav_file.
        3. Проверка тип фала (mine) на соответствие wav."""

        if not isinstance(file, StarletteUploadFile):
            raise ValueError(f"Expected UploadFile, received: {type(file)}")

        if file.size > Settings().size_wav_file:
            raise ValueError(
                f"Too large file to upload, maximum size {Settings().size_wav_file // 1024 // 1024} Mb: {file.size}"
            )

        if type_file := filetype.guess(file.file):
            if type_file.extension == 'wav':
                return file
            raise ValueError(f"Invalid file type: {type_file.extension}. The `wav` type is expected.")
        raise ValueError(f"Unknown file type")

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
