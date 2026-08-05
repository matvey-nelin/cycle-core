from fastapi import Request
from fastapi.responses import JSONResponse

from domain.exceptions import DomainError
from services.exceptions import ServiceError


def domain_error_handler(request: Request, exception: DomainError) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={"error": {"code": exception.error_code, "message": exception.message}},
    )


def service_error_handler(request: Request, exception: ServiceError) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={"error": {"code": exception.error_code, "message": exception.message}},
    )
