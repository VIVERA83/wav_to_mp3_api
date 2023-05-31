"""Views сервиса авторизации (AUTH)"""

from typing import Any

from auth.schemes import (
    OkSchema,
    UserSchemaLogin,
    UserSchemaOut,
    UserSchemaRegistration,
)
from auth.utils import update_session
from core.components import Request
from fastapi import APIRouter, HTTPException, status

auth_route = APIRouter()


@auth_route.post(
    "/create_user",
    summary="Регистрация нового пользователя",
    description="Регистрация нового пользователя в сервисе.",
    response_description="Анкетные данные пользователдя, кроме секретных данных.",
    tags=["AUTH"],
    response_model=UserSchemaOut,
)
async def create_user(request: "Request", user: UserSchemaRegistration) -> Any:
    """Создать пользователя."""
    new_user = await request.app.store.auth.create_user(**user.dict())
    update_session(request, new_user)
    return UserSchemaOut.from_orm(new_user)


@auth_route.post(
    "/login",
    summary="Авторизация",
    description="Авторизация пользователя в сервисе.",
    response_description="Анкетные данные пользователдя, кроме секретных данных.",
    tags=["AUTH"],
    response_model=UserSchemaOut,
)
async def login(request: "Request", user: UserSchemaLogin) -> Any:
    """Создать пользователя."""
    if user_db := await request.app.store.auth.get_user_by_email(user.email):
        if user_db.password == user.password:
            update_session(request, user_db)
            return UserSchemaOut.from_orm(user_db)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The user or password is incorrect",
    )


@auth_route.get(
    "/logout",
    summary="Выход",
    description="Выход из системы, что бы снова пользоваться сервисом необходимо будет снова авторизироваться.",
    tags=["AUTH"],
    response_model=OkSchema,
)
async def logout(request: "Request") -> Any:
    """Выход их системы."""
    del request.session["token"]
    return OkSchema()
