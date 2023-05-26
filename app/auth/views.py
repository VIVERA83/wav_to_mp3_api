"""Views сервиса авторизации (AUTH)"""
from typing import Any

from auth.schemes import UserSchemaIn, UserSchemaOut
from core.components import Request
from fastapi import APIRouter

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
    new_user = await request.app.store.auth.create_user(**user.dict())
    return UserSchemaOut(
        user_name=new_user.user_name,
        email=new_user.email,
        id=new_user.id,
        token=new_user.token,
    )
