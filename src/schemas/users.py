from pydantic import BaseModel, Field


class UserRequestAdd(BaseModel):
    email: str = Field(description="Электронная почта")
    password: str = Field(description="Пароль пользователя")

class UserAdd(BaseModel):
    email: str = Field(description="Электронная почта")
    hashed_password: str = Field(description="Зашифрованный пароль пользователя")

class User(BaseModel):
    id: int
    email: str = Field(description="Электронная почта")