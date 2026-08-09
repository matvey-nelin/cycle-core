from sqlalchemy.orm import Mapped

from infrastructure.models.base import Base, str_100, uuid7_pk


class AgonistORM(Base):
    __tablename__ = "agonists"

    id: Mapped[uuid7_pk]
    name: Mapped[str_100]
