from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

from backend.config import get_settings


# declarative base class
class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=get_settings().db.naming_convention,
    )
