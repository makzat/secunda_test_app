import uuid

from sqlalchemy import DECIMAL, ForeignKey, Text, text, types
from sqlalchemy.orm import Mapped, Relationship, mapped_column, relationship

from backend.models.base import Base


class Office(Base):
    __tablename__ = 'office'

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    address: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[float] = mapped_column(DECIMAL(10, 7), nullable=False)
    longitude: Mapped[float] = mapped_column(DECIMAL(10, 7), nullable=False)
    organization_id: Mapped[uuid.UUID] = mapped_column(types.Uuid, ForeignKey('organization.id'))
    organization: Relationship[list['Office']] = relationship(  # type: ignore # noqa: F821
        'Organization',
        back_populates='office',
        lazy='joined',
    )
