from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Organization
from backend.repository import OrganizationRepositoryProtocol
from backend.schemas.organizations import Coordinates
from backend.usecase.exceptions import NoDataOrganization


class OrganizationUseCaseProtocol(Protocol):
    session: AsyncSession
    repository: OrganizationRepositoryProtocol

    async def get_organization_by_id(self, organization_id: str) -> Organization: ...

    async def get_organization_by_name(self, name: str) -> Organization: ...

    async def get_organization_by_address(self, address: str) -> list[Organization]: ...

    async def get_organization_by_activity(self, activity: str) -> list[Organization]: ...

    async def get_organization_by_coordinates(self, coordinates: Coordinates) -> list[Organization]: ...

    async def get_organization_by_activity_tree(self, activity_path: str) -> list[Organization]: ...


class OrganizationUseCasee:
    def __init__(
        self,
        repository: OrganizationRepositoryProtocol,
    ):
        self.repository = repository

    async def get_organization_by_id(self, organization_id: str) -> Organization:
        organization = await self.repository.get_organization_by_id(organization_id=organization_id)

        if not organization:
            raise NoDataOrganization()

        return organization

    async def get_organization_by_name(self, name: str) -> Organization:
        organization = await self.repository.get_organization_by_name(name=name)

        if not organization:
            raise NoDataOrganization()

        return organization

    async def get_organization_by_address(self, address: str) -> list[Organization]:
        organizations = await self.repository.get_organizations_by_address(address=address)
        return organizations

    async def get_organization_by_activity(self, activity: str) -> list[Organization]:
        organizations = await self.repository.get_organization_by_activity(activity=activity)
        return organizations

    async def get_organization_by_coordinates(self, coordinates: Coordinates) -> list[Organization]:
        organizations = await self.repository.get_organizations_by_coordinates_with_radius(coordinates=coordinates)
        return organizations

    async def get_organization_by_activity_tree(self, activity_path: str) -> list[Organization]:
        organizations = await self.repository.get_organizations_by_activity_tree(activity_path=activity_path)
        return organizations
