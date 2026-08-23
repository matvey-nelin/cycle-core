from pydantic import UUID7, BaseModel, ConfigDict, Field


class ExerciseResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID7 = Field(examples=["019fcbf6-6d37-7264-b758-433859fb5e28"])
    name: str = Field(min_length=1, max_length=100, examples=["Bench press"])
    agonist_ids: list[UUID7] = Field(default=list())


class ExerciseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100, examples=["Bench press"])


class ExerciseUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100, examples=["Bench press"])
