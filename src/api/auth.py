from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Body, HTTPException
from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserAdd, UserRequestAdd
from passlib.context import CryptContext
import jwt

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= ({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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

@router.post('/login')
async def login_user(user_data: UserRequestAdd):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_by_id(email=user_data.email)
    if not user:
        raise HTTPException(status_code=401, detail='Пользователя с такими данными не существует')    
    access_token = create_access_token({'user_id': user.id})
    return {'access_token': access_token}