from uuid import UUID

from fastapi import APIRouter, Depends, Path

from api.dependencies import get_exercise_service
from api.schemas.exercise import ExerciseCreate, ExerciseResponse
from services.exercise_service import ExerciseService

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/{exercise_id}", response_model=ExerciseResponse, status_code=200)
async def read_exercise(
    exercise_id: UUID = Path(..., examples=["019fcbf6-6d37-7264-b758-433859fb5e28"]),
    service: ExerciseService = Depends(get_exercise_service),
):
    return await service.get_exercise(exercise_id)


@router.post("", status_code=201)
async def create_exercise(exercise: ExerciseCreate, service: ExerciseService = Depends(get_exercise_service)):
    exercise_id = await service.create_exercise(exercise.name)
    return {"status": "success", "exercise_id": exercise_id}


@router.patch("/{exercise_id}", status_code=204)
async def update_exercise(
    exercise: ExerciseCreate,
    exercise_id: UUID = Path(..., examples=["019fcbf6-6d37-7264-b758-433859fb5e28"]),
    service: ExerciseService = Depends(get_exercise_service),
):
    await service.update_exercise(exercise_id, exercise.name)


@router.post("/{exercise_id}/agonists/{agonist_id}", status_code=204)
async def add_agonist(
    exercise_id: UUID = Path(..., examples=["019fcbf6-6d37-7264-b758-433859fb5e28"]),
    agonist_id: UUID = Path(..., examples=["019fcbf6-6d37-7264-b758-433859fb5e28"]),
    service: ExerciseService = Depends(get_exercise_service),
):
    await service.add_agonist(exercise_id, agonist_id)


@router.delete("/{exercise_id}/agonists/{agonist_id}", status_code=204)
async def remove_agonist(
    exercise_id: UUID = Path(..., examples=["019fcbf6-6d37-7264-b758-433859fb5e28"]),
    agonist_id: UUID = Path(..., examples=["019fcbf6-6d37-7264-b758-433859fb5e28"]),
    service: ExerciseService = Depends(get_exercise_service),
):
    await service.remove_agonist(exercise_id, agonist_id)
