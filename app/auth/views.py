"""Views сервиса авторизации (AUTH)"""
from typing import Any

from auth.schemes import UserSchemaIn, UserSchemaOut
from core.components import Request
from fastapi import APIRouter
from icecream import ic

auth_route = APIRouter()


@auth_route.post(
    "/create_user",
    summary="Регистрация нового пользователя",
    description="Регистрация нового пользователя в сервисе.",
    response_description="Анкетные данные пользователдя, кроме секретных данных.",
    tags=["POST"],
    response_model=UserSchemaOut,

)
async def create_user(request: "Request", user: UserSchemaIn) -> Any:
    """Создать пользователя."""
    from uuid import uuid4
    return UserSchemaOut(id=uuid4(), token=uuid4())
