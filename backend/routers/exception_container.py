from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic_core._pydantic_core import ValidationError

from backend.usecase.exceptions import NoDataOrganization, NoDataOrganizations


def exception_container(app: FastAPI) -> FastAPI:
    @app.exception_handler(Exception)
    async def exception_500_code_server(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Server Error"},
        )

    @app.exception_handler(NoDataOrganization)
    async def not_found_organization_exception_handler(request: Request, exc: NoDataOrganization) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)})

    @app.exception_handler(NoDataOrganizations)
    async def not_found_organizations_exception_handler(request: Request, exc: NoDataOrganizations) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)})

    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handeler(request: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": str(exc)})

    return app
