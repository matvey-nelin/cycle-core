from repositories.workout_repositories import InMemoryWorkoutRepository
from services.workout_service import WorkoutService

repository = InMemoryWorkoutRepository()


def get_workout_service() -> WorkoutService:
    return WorkoutService(repository)
