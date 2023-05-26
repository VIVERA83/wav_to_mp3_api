"""Middleware приложения."""
import traceback
from typing import TYPE_CHECKING

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from http import HTTPStatus

if TYPE_CHECKING:
    from core.components import Application, Request


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Обработка внутренних ошибок при выпоолнение обработсиков запроса."""

    async def dispatch(self, request: "Request", call_next: RequestResponseEndpoint):
        """Обрапботка ошибок при мполнении handlers (views)."""
        try:
            response = await call_next(request)
            # response.headers["Custom"] = "Example"
            return response
        except Exception as error:
            if isinstance(error, IntegrityError):
                content = {
                    "detail": "UnProcessable Entity",
                    "message": "Perhaps one of the parameters does not meet the uniqueness rules",
                }
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                content = {
                    "detail": "Internal server error",
                    "message": "The server is temporarily unavailable try contacting later",
                }
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            if request.app.settings.logging.traceback:
                request.app.logger.error(traceback.format_exc())
            else:
                request.app.logger.error(f"{request.url=}, {error=}")
            return JSONResponse(content=content, status_code=status_code)


class ErrorContentLengthMiddleware(BaseHTTPMiddleware):
    """Проверка на размер получаемого Request."""

    async def dispatch(self, request: "Request", call_next: RequestResponseEndpoint):
        """Проверка на допустимый размер запроса.

        Макисальный размер на получаемый контент указыветсяв в настройках Settings."""

        max_size = request.app.settings.content_length + 300  # на служебные данные
        if max_size < int(request.headers.get('Content-Length')):
            return JSONResponse(content={"detail": "Request Entity Too Large",
                                         "message": "Too large file to upload, maximum size 1MB", },
                                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        return await call_next(request)


def setup_middleware(app: "Application"):
    """Настройка потключаемый Middleware."""
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(ErrorContentLengthMiddleware)
