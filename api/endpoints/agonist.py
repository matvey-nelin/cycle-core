from uuid import UUID

from fastapi import APIRouter, Depends, Path

from api.dependencies import get_agonist_service
from api.schemas.agonist import AgonistCreate, AgonistResponse, AgonistUpdate
from services.agonist_service import AgonistService

router = APIRouter(prefix="/agonists", tags=["agonists"])


@router.get("/{agonist_id}", response_model=AgonistResponse, status_code=200)
async def read_agonist(
    agonist_id: UUID = Path(..., examples=["019fcbf6-6d37-7264-b758-433859fb5e28"]),
    service: AgonistService = Depends(get_agonist_service),
):
    return await service.get_agonist(agonist_id)


@router.post("", status_code=201)
async def create_agonist(agonist: AgonistCreate, service: AgonistService = Depends(get_agonist_service)):
    agonist_id = await service.create_agonist(agonist.name)
    return {"status": "success", "agonist_id": agonist_id}


@router.patch("/{agonist_id}", status_code=204)
async def update_agonist(
    agonist: AgonistUpdate,
    agonist_id: UUID = Path(..., examples=["019fcbf6-6d37-7264-b758-433859fb5e28"]),
    service: AgonistService = Depends(get_agonist_service),
):
    await service.update_agonist(agonist_id, agonist.name)
