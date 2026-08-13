from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.models.agonist import AgonistORM
from infrastructure.models.base import Base, str_100, uuid7_pk


class ExerciseAgonistORM(Base):
    __tablename__ = "exercise_agonist"

    exercise_id: Mapped[UUID] = mapped_column(ForeignKey("exercises.id", ondelete="CASCADE"), primary_key=True)
    agonist_id: Mapped[UUID] = mapped_column(ForeignKey("agonists.id", ondelete="CASCADE"), primary_key=True)


class ExerciseORM(Base):
    __tablename__ = "exercises"

    id: Mapped[uuid7_pk]
    name: Mapped[str_100]

    agonists: Mapped[list["AgonistORM"]] = relationship(
        secondary=ExerciseAgonistORM.__tablename__,
        lazy="raise",
        order_by="AgonistORM.name.asc()",
    )
