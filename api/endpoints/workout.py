from uuid import UUID

from fastapi import APIRouter, Depends, Path

from api.dependencies import get_workout_service
from api.schemas.workout import WorkoutCreate, WorkoutResponse, WorkoutSetCreate
from services.workout_service import WorkoutService

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.get("/{workout_id}", response_model=WorkoutResponse, status_code=200)
def read_workout(
    workout_id: UUID = Path(..., examples=["019fcbf6-6d37-7264-b758-433859fb5e28"]),  # noqa: B008
    service: WorkoutService = Depends(get_workout_service),  # noqa: B008
):
    return service.get_workout(workout_id)


@router.post("/", status_code=201)
def create_workout(
    workout: WorkoutCreate,
    service: WorkoutService = Depends(get_workout_service),  # noqa: B008
):
    created_workout_id = service.create_workout(workout.start_time, workout.end_time)

    return {"status": "success", "workout_id": created_workout_id}


@router.post("/{workout_id}/sets", status_code=201)
def create_workout_set(
    workout_set: WorkoutSetCreate,
    workout_id: UUID = Path(..., examples=["019fcbf6-6d37-7264-b758-433859fb5e28"]),  # noqa: B008
    service: WorkoutService = Depends(get_workout_service),  # noqa: B008
):
    service.create_workout_set(
        workout_id, workout_set.exercise_id, workout_set.reps, workout_set.weight
    )

    return {"status": "success"}
