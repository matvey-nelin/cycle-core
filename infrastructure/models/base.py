from datetime import datetime
from typing import Annotated
from uuid import UUID

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, mapped_column
from uuid6 import uuid7

uuid7_pk = Annotated[UUID, mapped_column(primary_key=True, default=uuid7)]
str_100 = Annotated[str, mapped_column(String(100))]


class Base(DeclarativeBase):
    type_annotation_map = {datetime: DateTime(timezone=True)}
