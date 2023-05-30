"""Middleware приложения."""
import traceback
from typing import TYPE_CHECKING

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import Response

if TYPE_CHECKING:
    from core.components import Application, Request


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Обработка внутренних ошибок при выпоолнение обработсиков запроса."""

    async def dispatch(
        self, request: "Request", call_next: RequestResponseEndpoint
    ) -> Response:
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
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
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


class AuthorizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: "Request", call_next: RequestResponseEndpoint
    ) -> Response:
        """Проверка прав доступа к запрашевоемумо ресурсу."""
        print("Dispatch")
        # доступ для всех
        free_access = [
            "/openapi.json",
            "/docs",
            "/docs/oauth2-redirect",
            "/redoc",
            "/create_user",
            "/login",
            "/record",
        ]
        request.token = request.session.get("token", None)
        if request.url.path in free_access:
            return await call_next(request)
        if request.token:
            if await request.app.store.auth.get_user_by_token(request.token):
                return await call_next(request)

        return JSONResponse(
            content={
                "detail": "Forbidden",
                "message": "Access denied, please log in",
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )


def setup_middleware(app: "Application"):
    """Настройка потключаемый Middleware."""
    app.add_middleware(AuthorizationMiddleware)
    app.add_middleware(SessionMiddleware, secret_key=app.settings.secret_key)
    app.add_middleware(ErrorHandlingMiddleware)
