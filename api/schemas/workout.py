import datetime

from pydantic import UUID7, BaseModel, ConfigDict, Field, model_validator


class WorkoutCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start_time: datetime.datetime | None = Field(
        default=None,
        examples=[
            1785830000,
            "2026-08-01 15:00:00, 2026-08-01T15:00:00Z, 2026-08-01T15:00:00+00:00",
        ],
    )
    end_time: datetime.datetime | None = Field(
        default=None,
        examples=[
            1785830000,
            "2026-08-01 16:00:00, 2026-08-01T15:00:00Z, 2026-08-01T16:00:00+00:00",
        ],
    )

    @model_validator(mode="after")
    def convert_to_utc(self):
        # Set timezone to utc if it's none or save as is
        if self.start_time:
            if self.start_time.tzinfo is None:
                self.start_time = self.start_time.replace(tzinfo=datetime.UTC)
            else:
                self.start_time = self.start_time.astimezone(tz=datetime.UTC)

        if self.end_time:
            if self.end_time.tzinfo is None:
                self.end_time = self.end_time.replace(tzinfo=datetime.UTC)
            else:
                self.end_time = self.end_time.astimezone(tz=datetime.UTC)

        return self


class WorkoutSetCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    exercise_id: UUID7 = Field(examples=["019fcbf6-6d37-7264-b758-433859fb5e28"])
    reps: int = Field(ge=0, default=0)
    weight: float = Field(ge=0, default=0)


class WorkoutSetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID7 = Field(examples=["019fcbf6-6d37-7264-b758-433859fb5e28"])
    exercise_id: UUID7 = Field(examples=["019fcbf6-6d37-7264-b758-433859fb5e28"])

    planned_reps: int = Field(examples=[12])
    planned_weight: float = Field(examples=[17.5])

    actual_reps: int = Field(examples=[12])
    actual_weight: float = Field(examples=[17.5])

    planned_tonnage: float = Field(examples=[655, 655.55])
    actual_tonnage: float = Field(examples=[655, 655.55])
    completion_percentage: float = Field(examples=[66.67, 125.26])


class WorkoutResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID7 = Field(examples=["019fcbf6-6d37-7264-b758-433859fb5e28"])

    planned_start_time: datetime.datetime | None = Field(examples=["2026-08-01T15:00:00Z"])
    planned_end_time: datetime.datetime | None = Field(examples=["2026-08-01T16:00:00Z"])

    actual_start_time: datetime.datetime | None = Field(examples=["2026-08-01T15:00:00Z"])
    actual_end_time: datetime.datetime | None = Field(examples=["2026-08-01T16:00:00Z"])

    planned_tonnage: float = Field(examples=[1720, 1720.55])
    actual_tonnage: float = Field(examples=[1720, 1720.55])
    completion_percentage: float = Field(examples=[66.67, 125.26])

    sets: list[WorkoutSetResponse]
