from pydantic import EmailStr
from sqlalchemy import select
from app.repositories.mappers.base import APIModelType, DataMapper
from app.repositories.mappers.mappers import UsersDataMapper
from app.models.users import UsersOrm
from app.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper: DataMapper = UsersDataMapper

    # Метод для получения пользователя с захэшированным паролем по email
    async def get_user_with_hashed_password(
        self, email: EmailStr
    ) -> APIModelType:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)
