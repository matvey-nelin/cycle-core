import datetime

import pytest
from sqlalchemy import text
from uuid6 import uuid7

from domain.workout.workout import Workout, WorkoutSet
from infrastructure.repositories.exceptions import IncorrectWorkoutIdError
from infrastructure.repositories.workout.sqlalchemy_workout_repository import (
    SQLAlchemyWorkoutRepository,
)

DETERMINED_UUID_1 = uuid7()
DETERMINED_UUID_2 = uuid7()
DETERMINED_UUID_3 = uuid7()
EXERCISE_UUID = uuid7()


@pytest.fixture
async def full_workout_in_db(session_factory) -> Workout:
    # Inserting the exercise for data integrity (workout set 'exercise_id' not nullable)
    async with session_factory() as seeder:
        await seeder.execute(
            text("INSERT INTO exercises (id, name) VALUES (:id, :name)"),
            {"id": EXERCISE_UUID, "name": "Squat"},
        )
        await seeder.commit()

    workout = Workout(
        datetime.datetime(2026, 8, 1, 12, 0, 0, tzinfo=datetime.UTC),
        datetime.datetime(2026, 8, 1, 13, 0, 0, tzinfo=datetime.UTC),
        datetime.datetime(2026, 8, 1, 12, 15, 0, tzinfo=datetime.UTC),
        datetime.datetime(2026, 8, 1, 13, 15, 0, tzinfo=datetime.UTC),
    )

    workout.add_set(EXERCISE_UUID, 12, 60, 15, 50)
    workout.add_set(EXERCISE_UUID, 8, 40, 5, 35)
    workout.add_set(EXERCISE_UUID, 6, 100, 6, 90)

    async with session_factory() as seeder:
        repo = SQLAlchemyWorkoutRepository(seeder)
        await repo.create(workout)
        await repo.session.commit()

    return workout


class TestWorkoutRepository:
    async def test_create_writes_full_graph(self, session_factory, full_workout_in_db):
        async with session_factory() as reader:
            workout: Workout = (
                await reader.execute(
                    text(
                        """SELECT id, planned_start_time, planned_end_time,
                        actual_start_time, actual_end_time FROM workouts WHERE id = :id"""
                    ),
                    {"id": full_workout_in_db.id},
                )
            ).one()
            sets: list[WorkoutSet] = (
                await reader.execute(
                    text(
                        '''SELECT workout_id, exercise_id, "order", planned_reps, planned_weight,
                        actual_reps, actual_weight
                        FROM workout_sets WHERE workout_id = :id ORDER BY "order"'''
                    ),
                    {"id": full_workout_in_db.id},
                )
            ).all()

        assert workout.planned_start_time == full_workout_in_db.planned_start_time
        assert workout.planned_end_time == full_workout_in_db.planned_end_time
        assert workout.actual_start_time == full_workout_in_db.actual_start_time
        assert workout.actual_end_time == full_workout_in_db.actual_end_time

        assert len(sets) == 3
        assert [wset.workout_id for wset in sets] == [full_workout_in_db.id for i in range(len(sets))]
        assert [wset.order for wset in sets] == [i for i in range(1, len(sets) + 1)]
        assert [wset.planned_reps for wset in sets] == [12, 8, 6]
        assert [wset.planned_weight for wset in sets] == [60, 40, 100]
        assert [wset.actual_reps for wset in sets] == [15, 5, 6]
        assert [wset.actual_weight for wset in sets] == [50, 35, 90]

    async def test_get_by_id_scalars(
        self,
        session_factory,
        full_workout_in_db,
    ):
        async with session_factory() as reader:
            repo = SQLAlchemyWorkoutRepository(reader)
            founded_workout = await repo.get_by_id(full_workout_in_db.id)

        assert founded_workout is not None
        assert founded_workout.id == full_workout_in_db.id
        assert founded_workout.planned_start_time == full_workout_in_db.planned_start_time
        assert founded_workout.planned_end_time == full_workout_in_db.planned_end_time
        assert founded_workout.actual_start_time == full_workout_in_db.actual_start_time
        assert founded_workout.actual_end_time == full_workout_in_db.actual_end_time

    async def test_get_by_id_sets(
        self,
        session_factory,
        full_workout_in_db,
    ):
        async with session_factory() as reader:
            repo = SQLAlchemyWorkoutRepository(reader)
            got_workout = await repo.get_by_id(full_workout_in_db.id)

        assert got_workout is not None
        for i in range(len(got_workout.sets)):
            assert got_workout.sets[i].workout_id == full_workout_in_db.sets[i].workout_id
            assert got_workout.sets[i].exercise_id == full_workout_in_db.sets[i].exercise_id
            assert got_workout.sets[i].order == full_workout_in_db.sets[i].order
            assert got_workout.sets[i].planned_reps == full_workout_in_db.sets[i].planned_reps
            assert got_workout.sets[i].planned_weight == full_workout_in_db.sets[i].planned_weight
            assert got_workout.sets[i].actual_reps == full_workout_in_db.sets[i].actual_reps
            assert got_workout.sets[i].actual_weight == full_workout_in_db.sets[i].actual_weight

    async def test_get_by_non_existent_id_filled_database(
        self,
        session_factory,
        full_workout_in_db,
    ):
        unknown_workout_id = DETERMINED_UUID_1

        async with session_factory() as reader:
            repo = SQLAlchemyWorkoutRepository(reader)
            founded_workout = await repo.get_by_id(unknown_workout_id)

        assert founded_workout is None

    async def test_get_by_non_existent_id_empty_database(
        self,
        session_factory,
    ):
        unknown_workout_id = DETERMINED_UUID_1

        async with session_factory() as reader:
            repo = SQLAlchemyWorkoutRepository(reader)
            founded_workout = await repo.get_by_id(unknown_workout_id)

        assert founded_workout is None

    async def test_update_scalars(
        self,
        session_factory,
        full_workout_in_db,
    ):
        # Take a recorded workout
        async with session_factory() as reader:
            repo = SQLAlchemyWorkoutRepository(reader)
            workout = await repo.get_by_id(full_workout_in_db.id)

        assert workout is not None

        # Change the received workout (firstly end times: else error)
        workout.planned_end_time = datetime.datetime(2026, 8, 10, 13, 0, 0, tzinfo=datetime.UTC)
        workout.planned_start_time = datetime.datetime(2026, 8, 10, 12, 0, 0, tzinfo=datetime.UTC)
        workout.actual_end_time = datetime.datetime(2026, 8, 10, 13, 15, 0, tzinfo=datetime.UTC)
        workout.actual_start_time = datetime.datetime(2026, 8, 10, 12, 15, 0, tzinfo=datetime.UTC)

        async with session_factory() as seeder:
            repo = SQLAlchemyWorkoutRepository(seeder)
            await repo.update(workout)
            await seeder.commit()

        # Assure that changes applied
        async with session_factory() as reader:
            repo = SQLAlchemyWorkoutRepository(reader)
            updated_workout = await repo.get_by_id(full_workout_in_db.id)

        assert updated_workout is not None
        assert updated_workout.planned_start_time == workout.planned_start_time
        assert updated_workout.planned_end_time == workout.planned_end_time
        assert updated_workout.actual_start_time == workout.actual_start_time
        assert updated_workout.actual_end_time == workout.actual_end_time

    async def test_update_set_deleted(
        self,
        session_factory,
        full_workout_in_db,
    ):
        # Take a recorded workout
        async with session_factory() as reader:
            repo = SQLAlchemyWorkoutRepository(reader)
            workout = await repo.get_by_id(full_workout_in_db.id)

        assert workout is not None

        # Change the received workout (firstly end times: else error)
        workout.remove_set(full_workout_in_db.sets[1].id)

        async with session_factory() as seeder:
            repo = SQLAlchemyWorkoutRepository(seeder)
            await repo.update(workout)
            await seeder.commit()

        # Assure that changes applied
        async with session_factory() as reader:
            repo = SQLAlchemyWorkoutRepository(reader)
            updated_workout = await repo.get_by_id(full_workout_in_db.id)

        assert updated_workout is not None
        assert len(updated_workout.sets) == 2
        assert [wset.order for wset in updated_workout.sets] == [1, 2]
        assert [wset.id for wset in updated_workout.sets] == [wset.id for wset in workout.sets]

    async def test_update_set_added(
        self,
        session_factory,
        full_workout_in_db,
    ):
        # Take a recorded workout
        async with session_factory() as reader:
            repo = SQLAlchemyWorkoutRepository(reader)
            workout = await repo.get_by_id(full_workout_in_db.id)

        assert workout is not None

        # Change the received workout (firstly end times: else error)
        workout.add_set(exercise_id=EXERCISE_UUID, planned_reps=20, planned_weight=0, actual_reps=18, actual_weight=0)

        async with session_factory() as seeder:
            repo = SQLAlchemyWorkoutRepository(seeder)
            await repo.update(workout)
            await seeder.commit()

        # Assure that changes applied
        async with session_factory() as reader:
            repo = SQLAlchemyWorkoutRepository(reader)
            updated_workout = await repo.get_by_id(full_workout_in_db.id)

        assert updated_workout is not None
        assert len(updated_workout.sets) == 4
        assert [wset.order for wset in updated_workout.sets] == [1, 2, 3, 4]
        assert [wset.id for wset in updated_workout.sets] == [wset.id for wset in workout.sets]

    async def test_update_set_changed(
        self,
        session_factory,
        full_workout_in_db,
    ):
        # Take a recorded workout
        async with session_factory() as reader:
            repo = SQLAlchemyWorkoutRepository(reader)
            workout = await repo.get_by_id(full_workout_in_db.id)

        assert workout is not None

        # Change the received workout (firstly end times: else error)
        workout.sets[0].planned_reps = 5
        workout.sets[0].planned_weight = 100
        workout.sets[0].actual_reps = 6
        workout.sets[0].actual_weight = 110

        async with session_factory() as seeder:
            repo = SQLAlchemyWorkoutRepository(seeder)
            await repo.update(workout)
            await seeder.commit()

        # Assure that changes applied
        async with session_factory() as reader:
            repo = SQLAlchemyWorkoutRepository(reader)
            updated_workout = await repo.get_by_id(full_workout_in_db.id)

        assert updated_workout is not None
        assert len(updated_workout.sets) == 3
        assert [wset.order for wset in updated_workout.sets] == [1, 2, 3]
        assert updated_workout.sets[0].planned_reps == workout.sets[0].planned_reps
        assert updated_workout.sets[0].planned_weight == workout.sets[0].planned_weight
        assert updated_workout.sets[0].actual_reps == workout.sets[0].actual_reps
        assert updated_workout.sets[0].actual_weight == workout.sets[0].actual_weight

    async def test_update_non_existent_workout(self, session_factory):
        workout = Workout()

        with pytest.raises(IncorrectWorkoutIdError):
            async with session_factory() as seeder:
                repo = SQLAlchemyWorkoutRepository(seeder)
                await repo.update(workout)
                await seeder.commit()
