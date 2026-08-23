from uuid import UUID

from fastapi import APIRouter, Depends, Path

from api.dependencies import get_workout_service
from api.schemas.workout import WorkoutCreate, WorkoutResponse, WorkoutSetCreate
from services.workout_service import WorkoutService

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.get("/{workout_id}", response_model=WorkoutResponse, status_code=200)
async def read_workout(
    workout_id: UUID = Path(..., examples=["019fcbf6-6d37-7264-b758-433859fb5e28"]),
    service: WorkoutService = Depends(get_workout_service),
):
    return await service.get_workout(workout_id)


@router.post("", status_code=201)
async def create_workout(
    workout: WorkoutCreate,
    service: WorkoutService = Depends(get_workout_service),
):
    workout_id = await service.create_workout(workout.start_time, workout.end_time)
    return {"status": "success", "workout_id": workout_id}


@router.post("/{workout_id}/sets", status_code=201)
async def create_workout_set(
    workout_set: WorkoutSetCreate,
    workout_id: UUID = Path(..., examples=["019fcbf6-6d37-7264-b758-433859fb5e28"]),
    service: WorkoutService = Depends(get_workout_service),
):
    workout_set_id = await service.add_workout_set(
        workout_id, workout_set.exercise_id, workout_set.reps, workout_set.weight
    )
    return {"status": "success", "workout_set_id": workout_set_id}


@router.delete("/{workout_id}/sets/{workout_set_id}", status_code=204)
async def remove_workout_set(
    workout_id: UUID = Path(..., examples=["019fcbf6-6d37-7264-b758-433859fb5e28"]),
    workout_set_id: UUID = Path(..., examples=["019fcbf6-6d37-7264-b758-433859fb5e28"]),
    service: WorkoutService = Depends(get_workout_service),
):
    await service.remove_workout_set(workout_id, workout_set_id)
