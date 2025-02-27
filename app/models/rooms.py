from typing import TYPE_CHECKING, List, Optional
from app.database import Base
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.facilities import FacilitiesOrm


class RoomsOrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)
    facilities: Mapped[Optional[List["FacilitiesOrm"]]] = relationship(
        back_populates="rooms",
        secondary="rooms_facilities",
    )
