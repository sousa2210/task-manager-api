
from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100,
    )
    description: str = Field(
        default="",
        max_length=500,
    )
    completed: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("O título não pode ficar vazio.")

        return value


class TaskUpdate(TaskCreate):
    pass


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    completed: bool



class TaskPartialUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=500,
    )
    completed: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("O título não pode ficar vazio.")

        return value


    model_config = ConfigDict(extra="forbid")
