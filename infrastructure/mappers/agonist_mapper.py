from domain.agonist.agonist import Agonist
from infrastructure.models.agonist import AgonistORM


class AgonistMapper:
    @staticmethod
    def to_domain(orm: AgonistORM) -> Agonist:
        return Agonist.reconstract(id=orm.id, name=orm.name)

    @staticmethod
    def to_orm(domain: Agonist) -> AgonistORM:
        return AgonistORM(id=domain.id, name=domain.name)
