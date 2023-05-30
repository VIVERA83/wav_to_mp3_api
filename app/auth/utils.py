"""Вспомогательные функции для модуля AUTH."""
from auth.models import UserModel
from core.components import Request


def update_session(request: "Request", user: UserModel):
    """Обновить сессию.

    Обновляем `token` и `user_id`.
    """
    request.session["token"] = user.token.hex
    request.session["user_id"] = user.token.hex
