import uuid

from sqlalchemy import VARCHAR, CheckConstraint, ForeignKey, text, types
from sqlalchemy.orm import Mapped, Relationship, mapped_column, relationship
from sqlalchemy_utils import LtreeType

from backend.models.base import Base


class OrganizationActivityAssociation(Base):
    __tablename__ = 'organization_activity_association'

    organization_id: Mapped[uuid.UUID] = mapped_column(types.Uuid, ForeignKey('organization.id'), primary_key=True)
    activity_id: Mapped[uuid.UUID] = mapped_column(types.Uuid, ForeignKey('activity.id'), primary_key=True)


class Activity(Base):
    __tablename__ = 'activity'

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    name: Mapped[str] = mapped_column(
        VARCHAR(50),
        nullable=False,
    )
    path: Mapped[str] = mapped_column(LtreeType, nullable=False)

    organizations: Relationship[list['Organization']] = relationship(  # type: ignore # noqa: F821
        secondary='organization_activity_association', back_populates='activities', viewonly=False
    )

    __table_args__ = (CheckConstraint('nlevel(path) <= 3', name='check_ltree_depth'),)
