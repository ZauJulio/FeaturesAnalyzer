from collections.abc import Mapping
from typing import Any, Literal, TypeVar

from pydantic import BaseModel as PydanticBaseModel


class BaseSchema(PydanticBaseModel):
    """Base class for FAORM models."""

    uid: str | None = None


SchemaType = TypeVar("SchemaType", bound=BaseSchema)


class ReferenceSchema(PydanticBaseModel):
    """Represents a reference to another model (similar to Mongoose's populate)."""

    _id: str
    from_table: str


class FAPreProcessorSchema(BaseSchema):
    """A preprocessor to prepare data for a model."""

    name: str
    params: Any
    data_hash: str | None = None


FAPreProcessorSchemaType = TypeVar(
    "FAPreProcessorSchemaType",
    bound=FAPreProcessorSchema,
)


class FAModelSchema(BaseSchema):
    """A preprocessor to prepare data for a model."""

    name: str
    params: Mapping[
        str,
        str
        | int
        | float
        | bool
        | list[str | int | float | bool]
        | dict[str, str | int | float | bool],
    ]
    data_hash: str | None = None

    pre_processors: list[str] = []


type SchemasKeys = Literal["FAPreProcessor", "FAModel"]
