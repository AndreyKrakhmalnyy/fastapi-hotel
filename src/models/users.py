from src.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class UsersOrm(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(100))