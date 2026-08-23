from infrastructure.database import AsyncSessionLocal
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from services.agonist_service import AgonistService
from services.exercise_service import ExerciseService
from services.workout_service import WorkoutService


def get_agonist_service() -> AgonistService:
    return AgonistService(SQLAlchemyUnitOfWork(AsyncSessionLocal))


def get_exercise_service() -> ExerciseService:
    return ExerciseService(SQLAlchemyUnitOfWork(AsyncSessionLocal))


def get_workout_service() -> WorkoutService:
    return WorkoutService(SQLAlchemyUnitOfWork(AsyncSessionLocal))
