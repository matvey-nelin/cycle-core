from pydantic import UUID7, BaseModel, ConfigDict, Field


class AgonistResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID7 = Field(examples=["019fcbf6-6d37-7264-b758-433859fb5e28"])
    name: str = Field(min_length=1, max_length=100, examples=["Pectoralis major"])


class AgonistCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100, examples=["Pectoralis major"])


class AgonistUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(min_length=1, max_length=100, examples=["Pectoralis major"])
