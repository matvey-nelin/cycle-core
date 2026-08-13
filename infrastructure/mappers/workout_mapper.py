from domain.workout.workout import Workout, WorkoutSet
from infrastructure.models.workout import WorkoutORM, WorkoutSetORM


class WorkoutSetMapper:
    @staticmethod
    def to_domain(orm: WorkoutSetORM) -> WorkoutSet:
        return WorkoutSet.reconstruct(
            id=orm.id,
            workout_id=orm.workout_id,
            exercise_id=orm.exercise_id,
            order=orm.order,
            planned_reps=orm.planned_reps,
            planned_weight=orm.planned_weight,
            actual_reps=orm.actual_reps,
            actual_weight=orm.actual_weight,
        )

    @staticmethod
    def to_orm(domain: WorkoutSet) -> WorkoutSetORM:
        return WorkoutSetORM(
            id=domain.id,
            workout_id=domain.workout_id,
            exercise_id=domain.exercise_id,
            order=domain.order,
            planned_reps=domain.planned_reps,
            planned_weight=domain.planned_weight,
            actual_reps=domain.actual_reps,
            actual_weight=domain.actual_weight,
        )


class WorkoutMapper:
    @staticmethod
    def to_domain(orm: WorkoutORM) -> Workout:
        return Workout.reconstruct(
            id=orm.id,
            planned_start_time=orm.planned_start_time,
            planned_end_time=orm.planned_end_time,
            actual_start_time=orm.actual_start_time,
            actual_end_time=orm.actual_end_time,
            sets=[WorkoutSetMapper.to_domain(wset) for wset in orm.sets],
        )

    @staticmethod
    def to_orm(domain: Workout) -> WorkoutORM:
        return WorkoutORM(
            id=domain.id,
            planned_start_time=domain.planned_start_time,
            planned_end_time=domain.planned_end_time,
            actual_start_time=domain.actual_start_time,
            actual_end_time=domain.actual_end_time,
            sets=[WorkoutSetMapper.to_orm(wset) for wset in domain.sets],
        )
