from pydantic import BaseModel, EmailStr, Field


class UserRequestAdd(BaseModel):
    email: EmailStr = Field(description="Электронная почта")
    password: str = Field(description="Пароль пользователя")

class UserAdd(BaseModel):
    email: EmailStr = Field(description="Электронная почта")
    hashed_password: str = Field(description="Зашифрованный пароль пользователя")
    

class User(BaseModel):
    id: int
    email: EmailStr = Field(description="Электронная почта")
 
class UserWithHashedPassword(User):
    hashed_password: str = Field(description="Зашифрованный пароль пользователя")