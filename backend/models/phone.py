import uuid

from sqlalchemy import VARCHAR, ForeignKey, text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base
from backend.models.organizations import Organization


class Phone(Base):
    __tablename__ = 'phone'

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    number: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    organization_id: Mapped[uuid.UUID] = mapped_column(types.Uuid, ForeignKey('organization.id'))
    organization: Mapped['Organization'] = relationship(  # type: ignore # noqa: F821
        'Organization', back_populates='phones'
    )
