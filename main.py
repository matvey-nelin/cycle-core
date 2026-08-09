import uvicorn  # noqa: I001
from fastapi import FastAPI

from api.endpoints.workout import router as workout_router
from api.exception_handlers import domain_error_handler, service_error_handler
from domain.exceptions import DomainError
from services.exceptions import ServiceError

from infrastructure.models.base import Base  # noqa: F401


app = FastAPI()

# Using precise base exception types for exception handlers
app.add_exception_handler(DomainError, domain_error_handler)  # type: ignore[arg-type]
app.add_exception_handler(ServiceError, service_error_handler)  # type: ignore[arg-type]

# Grouping endpoints into routers by logical responsibility
app.include_router(workout_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
