import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Security
from pydantic import TypeAdapter

from backend.di import get_organization_usecase
from backend.schemas.organizations import Coordinates, OrganizationSchema, OrganizationsSchema
from backend.security import check_api_key
from backend.usecase.organization import OrganizationUseCaseProtocol

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Security(check_api_key)])


@router.get(
    '/organization/{organization_id}',
    response_model=OrganizationSchema,
    description='Поиск организаций по айди организации.',
)
async def get_organization_by_id(
    organization_id: str,
    organization_usecase: Annotated[OrganizationUseCaseProtocol, Depends(get_organization_usecase)],
) -> OrganizationSchema:
    organization = await organization_usecase.get_organization_by_id(organization_id=organization_id)
    return OrganizationSchema.model_validate(organization)


@router.get('/organization/{name}', response_model=OrganizationSchema, description='Поиск организаций по названию.')
async def get_organization_by_name(
    name: str,
    organization_usecase: Annotated[OrganizationUseCaseProtocol, Depends(get_organization_usecase)],
) -> OrganizationSchema:
    organization = await organization_usecase.get_organization_by_name(name=name)
    return OrganizationSchema.model_validate(organization)


@router.get(
    '/organization/office/{office_address}',
    response_model=OrganizationsSchema,
    description='Cписок всех организаций находящихся в конкретном здании.',
)
async def get_organization_by_address(
    organization_usecase: Annotated[OrganizationUseCaseProtocol, Depends(get_organization_usecase)],
    office_address: str,
) -> OrganizationsSchema:
    organizations = await organization_usecase.get_organization_by_address(address=office_address)
    return OrganizationsSchema(organizations=TypeAdapter(list[OrganizationSchema]).validate_python(organizations))


@router.get(
    '/organization/activity/{activity_name}',
    response_model=OrganizationsSchema,
    description='Cписок всех организаций, которые относятся к указанному виду деятельности.',
)
async def get_organization_by_activity(
    organization_usecase: Annotated[OrganizationUseCaseProtocol, Depends(get_organization_usecase)],
    activity_name: str,
) -> OrganizationsSchema:
    organizations = await organization_usecase.get_organization_by_activity(activity=activity_name)
    return OrganizationsSchema(organizations=TypeAdapter(list[OrganizationSchema]).validate_python(organizations))


@router.get(
    '/organization/search-radius',
    response_model=OrganizationsSchema,
    description='Cписок организаций, которые находятся в заданном радиусе относительно указанной точки на карте.',
)
async def get_organization_by_search_radius(
    organization_usecase: Annotated[OrganizationUseCaseProtocol, Depends(get_organization_usecase)],
    coordinates: Coordinates = Query(),
) -> OrganizationsSchema:
    organizations = await organization_usecase.get_organization_by_coordinates(coordinates=coordinates)
    return OrganizationsSchema(organizations=TypeAdapter(list[OrganizationSchema]).validate_python(organizations))


@router.get(
    '/organizations/activity-tree/{activity_name}',
    response_model=OrganizationsSchema,
    description='Искать организации по виду деятельности и потомков этой деятельности',
)
async def get_organization_by_activity_tree(
    organization_usecase: Annotated[OrganizationUseCaseProtocol, Depends(get_organization_usecase)],
    activity_name: str,
) -> OrganizationsSchema:
    organizations = await organization_usecase.get_organization_by_activity_tree(activity_path=activity_name)
    q = OrganizationsSchema(organizations=TypeAdapter(list[OrganizationSchema]).validate_python(organizations))
    return q
