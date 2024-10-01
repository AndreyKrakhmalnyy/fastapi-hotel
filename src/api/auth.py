from fastapi import APIRouter, Body
from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserAdd, UserRequestAdd
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/register')
async def register_user(
    user_data: UserRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Иван",
                "value": {"email": "ivan10@mail.ru", "password": "abcdefg123"},
            },
            "2": {
                "summary": "Андрей",
                "value": {"email": "andrey10@mail.ru", "password": "afdsef34"},
            },
            "3": {
                "summary": "Виктория",
                "value": {"email": "victoria10@mail.ru", "password": "wefwegr4@%264"},
            },
        }
    )):
    hashed_password = pwd_context.hash(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add_one(new_user_data)
        await session.commit()
        
    return {"status": "OK"}