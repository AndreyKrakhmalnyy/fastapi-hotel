from pydantic import BaseModel, EmailStr, Field


class UserRequestAdd(BaseModel):
    email: EmailStr = Field(description="Электронная почта")
    password: str = Field(description="Пароль пользователя")


class UserAdd(BaseModel):
    email: EmailStr = Field(description="Электронная почта")
    hashed_password: str = Field(
        description="Зашифрованный пароль пользователя"
    )


class UserIn(BaseModel):
    id: int
    email: EmailStr = Field(description="Электронная почта")


class UserOut(UserIn):
    hashed_password: str = Field(
        description="Зашифрованный пароль пользователя"
    )
