from fastapi import APIRouter, Body, HTTPException, Response
from src.api.dependencies import UserIdDep, UserTokenDep, DBDep
from src.services.auth import AuthService
from src.schemas.users import UserAdd, UserRequestAdd


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
        user = await db.users.get_one_or_none(id=user_id)
        return user

@router.post("/register")
async def register_user(
    db: DBDep, 
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
    )
):
    hashed_password = AuthService().hash_password(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
    await db.users.add_one(new_user_data)
    await db.commit()
    return {"status": "OK"}

@router.post("/login")
async def login_user(db: DBDep, user_data: UserRequestAdd, response: Response):
        user = await db.users.get_user_with_hashed_password(
            email=user_data.email
        )
        if not user:
            raise HTTPException(
                status_code=401, detail="Пользователь с такой почтой не найден"
            )
        if not AuthService().verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}

@router.post("/logout")
async def logout_user(token: UserTokenDep, response: Response):
    return AuthService().logout_session(token, response)