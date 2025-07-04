from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, select, cast
from sqlalchemy import String

from backend.models import Activity, Office, Organization, OrganizationActivityAssociation
from backend.schemas.organizations import Coordinates


class OrganizationRepositoryProtocol(Protocol):
    session: AsyncSession

    async def get_organization_by_id(self, organization_id: str) -> Organization: ...

    async def get_organization_by_name(self, name: str) -> Organization: ...

    async def get_organizations_by_address(self, address: str) -> list[Organization]: ...

    async def get_organization_by_activity(self, activity: str) -> list[Organization]: ...

    async def get_organizations_by_coordinates_with_radius(self, coordinates: Coordinates) -> list[Organization]: ...

    async def get_organizations_by_activity_tree(self, activity_path: str) -> list[Organization]: ...


class OrganizationRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_organization_by_id(self, organization_id: str) -> Organization | None:
        result = await self.session.execute(select(Organization).where(Organization.id == organization_id))
        organization: Organization | None = result.scalars().unique().one_or_none()
        return organization

    async def get_organization_by_name(self, name: str) -> Organization | None:
        result = await self.session.execute(select(Organization).where(Organization.name == name))
        organization: Organization | None = result.scalars().one_or_none()
        return organization

    async def get_organizations_by_address(self, address: str) -> list[Organization]:
        result = await self.session.execute(select(Organization).join(Office).where(Office.address == address))
        organizations: list[Organization] = list(result.scalars().unique().all())
        return organizations

    async def get_organizations_by_activity(self, activity: str) -> list[Organization]:
        result = await self.session.execute(
            select(Organization).join(OrganizationActivityAssociation).join(Activity).where(Activity.name == activity)
        )
        organizations: list[Organization] = list(result.scalars().all())
        return organizations

    async def get_organizations_by_coordinates_with_radius(self, coordinates: Coordinates) -> list[Organization]:
        result = await self.session.execute(
            select(Organization)
            .join(Office)
            .where(
                func.sqrt(
                    func.pow(Office.latitude - coordinates.latitude, 2)
                    + func.pow(Office.longitude - coordinates.longitude, 2)
                )
                <= coordinates.radius
            )
        )
        organizations: list[Organization] = list(result.scalars().all())
        return organizations

    async def get_organizations_by_activity_tree(self, activity_path: str) -> list[Organization]:
        result = await self.session.execute(
            select(Organization)
            .join(OrganizationActivityAssociation)
            .join(Activity)
            .where(func.ltree(Activity.path).op('<@')(func.ltree(activity_path)))
        )
        organizations: list[Organization] = list(result.unique().scalars().all())
        return organizations
