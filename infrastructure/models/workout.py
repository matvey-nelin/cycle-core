from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.models.base import Base, uuid7_pk


class WorkoutSetORM(Base):
    __tablename__ = "workout_sets"

    id: Mapped[uuid7_pk]
    order: Mapped[int]
    planned_reps: Mapped[int] = mapped_column(default=0)
    planned_weight: Mapped[float] = mapped_column(default=0)
    actual_reps: Mapped[int] = mapped_column(default=0)
    actual_weight: Mapped[float] = mapped_column(default=0)

    workout_id: Mapped[UUID] = mapped_column(ForeignKey("workouts.id", ondelete="CASCADE"))
    exercise_id: Mapped[UUID] = mapped_column(ForeignKey("exercises.id", ondelete="RESTRICT"))


class WorkoutORM(Base):
    __tablename__ = "workouts"

    id: Mapped[uuid7_pk]
    planned_start_time: Mapped[datetime | None]
    planned_end_time: Mapped[datetime | None]
    actual_start_time: Mapped[datetime | None]
    actual_end_time: Mapped[datetime | None]

    sets: Mapped[list["WorkoutSetORM"]] = relationship(
        cascade="all, delete-orphan", lazy="raise", order_by="WorkoutSetORM.order.asc()"
    )
