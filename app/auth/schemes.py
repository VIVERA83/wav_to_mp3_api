"""Schemas сервиса Авторизации (AUTH)."""

from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class BaseUserSchema(BaseModel):
    user_name: str = Field(title="Имя пользователя", example="Василий Алибабаевич")
    email: EmailStr = Field(title="email адрес пользователя, уникальный элемент.")


class UserSchemaIn(BaseUserSchema):
    """Schema пользователя при регистрации."""
    ...


class UserSchemaOut(BaseUserSchema):
    id: UUID = Field(
        description="уникальный `id` номер пользователя, задается автоматически",
        title="Id пользователя",
        example="a17b2315-5bb8-40d3-8d8a-2d48b6c3144e",
    )
    token: UUID = Field(description="токен пользователя, задается автоматически",
                        title="token пользователя",
                        example="a17b2315-5bb8-40d3-8d8a-2d48b6c3144e", )
