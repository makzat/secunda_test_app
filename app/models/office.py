import uuid

from sqlalchemy import DECIMAL, Text, text, types
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Office(Base):
    __tablename__ = "office"

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    address: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[float] = mapped_column(DECIMAL(10, 7), nullable=False)
    longitude: Mapped[float] = mapped_column(DECIMAL(10, 7), nullable=False)
