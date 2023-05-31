"""Schemas сервиса Авторизации (AUTH)."""
from hashlib import sha256
from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, SecretStr, validator


class BaseUserSchema(BaseModel):
    user_name: str = Field(title="Имя пользователя", example="Василий Алибабаевич")
    email: EmailStr = Field(title="email адрес пользователя, уникальный элемент.")

    class Config:
        orm_mode = True


class UserSchemaRegistration(BaseUserSchema):
    """Schema пользователя при регистрации."""

    password: SecretStr = Field(title="Пароль", example="password")
    password_confirmation: SecretStr = Field(
        title="Пароль", example="password", exclude=True
    )

    @validator("password")
    def hash_passwords(cls, password: SecretStr) -> str:  # noqa cls
        """Хэшируем пароль."""
        return sha256(password.get_secret_value().encode("utf-8")).hexdigest()

    @validator("password_confirmation")
    def passwords_match(
        cls, password_confirmation: SecretStr, values: dict[str, Any]
    ) -> str:  # noqa cls
        """Проверка пароля на совпадение."""
        password = sha256(
            password_confirmation.get_secret_value().encode("utf-8")
        ).hexdigest()
        if password != values["password"]:
            raise ValueError("passwords do not match")
        return password_confirmation


class UserSchemaOut(BaseUserSchema):
    id: UUID = Field(
        description="уникальный `id` номер пользователя, задается автоматически",
        title="Id пользователя",
        example="a17b2315-5bb8-40d3-8d8a-2d48b6c3144e",
    )


class UserSchemaLogin(BaseModel):
    email: EmailStr = Field(title="email адрес пользователя, уникальный элемент.")
    password: SecretStr = Field(
        title="Пароль",
        example="password",
        description="Пароль, который был указан при регистрации пользователя",
    )

    @validator("password")
    def hash_passwords(cls, password: SecretStr) -> str:  # noqa cls
        """Хэшируем пароль."""
        return sha256(password.get_secret_value().encode("utf-8")).hexdigest()


class OkSchema(BaseModel):
    detail: str = "OK 200"
    message: str = "Successfully"
