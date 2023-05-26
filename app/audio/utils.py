from typing import Any, Callable, Iterable, Type

from core.settings import Settings
from fastapi import File
from starlette.datastructures import UploadFile as StarletteUploadFile


class UploadFile(StarletteUploadFile):
    @classmethod
    def __get_validators__(cls: Type["UploadFile"]) -> Iterable[Callable[..., Any]]:
        yield cls.validate

    @classmethod
    def validate(cls: Type["UploadFile"], file: File) -> Any:
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
