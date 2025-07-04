from fastapi import Depends

from backend.repository import OrganizationRepository, OrganizationRepositoryProtocol
from backend.services import db_helper
from backend.usecase import OrganizationUseCasee, OrganizationUseCaseProtocol


# creating objects for periodic tasks
def get_database_repository(
    session=Depends(db_helper.session_getter_context_manager),
) -> OrganizationRepositoryProtocol:
    return OrganizationRepository(session=session)


def get_organization_usecase(
    repository=Depends(get_database_repository),
) -> OrganizationUseCaseProtocol:
    return OrganizationUseCasee(
        repository=repository,
    )
