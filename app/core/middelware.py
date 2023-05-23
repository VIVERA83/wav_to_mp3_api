"""Middleware приложения."""
import traceback
from typing import TYPE_CHECKING

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.middleware.base import BaseHTTPMiddleware

if TYPE_CHECKING:
    from core.components import Application, Request


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: "Request", call_next):
        try:
            response = await call_next(request)
            response.headers["Custom"] = "Example"
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


def setup_middleware(app: "Application"):
    """Настройка потключаемый Middleware."""
    app.add_middleware(ErrorHandlingMiddleware)
