# Import base for all models class for do them available from the outside
# ruff: noqa F401
from infrastructure.models.base import Base


# Import all models for registred them in metadata of base class
from infrastructure.models.agonist import AgonistORM
from infrastructure.models.exercise import ExerciseORM, ExerciseAgonistORM

from infrastructure.models.workout import WorkoutORM, WorkoutSetORM
