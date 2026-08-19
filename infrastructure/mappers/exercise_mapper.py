from domain.exercise.exercise import Exercise
from infrastructure.models.agonist import AgonistORM
from infrastructure.models.exercise import ExerciseORM


class ExerciseMapper:
    @staticmethod
    def to_domain(orm: ExerciseORM) -> Exercise:
        return Exercise.reconstruct(id=orm.id, name=orm.name, agonist_ids=[agonist.id for agonist in orm.agonists])

    @staticmethod
    def to_orm(domain: Exercise, agonists: list[AgonistORM]) -> ExerciseORM:
        return ExerciseORM(id=domain.id, name=domain.name, agonists=agonists)
