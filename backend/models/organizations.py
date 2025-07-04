import uuid

from sqlalchemy import VARCHAR, text, types
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, Relationship, mapped_column, relationship

from backend.models.base import Base


class Organization(Base):
    __tablename__ = 'organization'

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    phones: Relationship[list['Phone']] = relationship(  # type: ignore # noqa: F821
        'Phone', back_populates='organization', lazy='joined', cascade='all, delete-orphan'
    )
    phones_number: AssociationProxy[list[str]] = association_proxy('phones', 'number')
    office: Relationship['Office'] = relationship(  # type: ignore # noqa: F821
        'Office', back_populates='organization', lazy='joined', cascade='all, delete-orphan'
    )
    office_address: AssociationProxy[str] = association_proxy('office', 'address')
    activities: Mapped[list['Activity']] = relationship(  # type: ignore # noqa: F821
        secondary='organization_activity_association',
        lazy='joined',
        back_populates='organizations',
    )
    activity_names: AssociationProxy[list[str]] = association_proxy('activities', 'path')
