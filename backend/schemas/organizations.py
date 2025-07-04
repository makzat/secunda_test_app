from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator, PlainValidator, PlainSerializer, WithJsonSchema, field_serializer
from sqlalchemy_utils import Ltree


LtreeField = Annotated[
    Ltree,
    PlainValidator(lambda v: Ltree(v)),
]

class Coordinates(BaseModel):
    latitude: float
    longitude: float
    radius: float


class OrganizationsGetParamsSchema(Coordinates): ...


class OrganizationSchema(BaseModel):
    id: str
    name: str
    phones_number: list[str]
    office_address: str
    activity_names: list[LtreeField]

    @field_validator('id', mode='before')
    @classmethod
    def uuid_to_string(cls, value: UUID) -> str:
        return str(value)

    @field_serializer('activity_names')
    def serialize_activity_names(self, value: list[LtreeField], _info) -> list[str]:
        result = set()
        for i in value:
            result.update(i.path.split('.'))
        return list(result)


    model_config = ConfigDict(from_attributes=True)


class OrganizationsSchema(BaseModel):
    organizations: list[OrganizationSchema]
