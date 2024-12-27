from app.database import Base
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column


class RoomsOrm(Base):
    __tablename__ = 'rooms'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)