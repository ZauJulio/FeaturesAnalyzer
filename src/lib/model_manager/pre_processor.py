import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic, TypeVar

from pandas import DataFrame

from lib.orm import db
from lib.orm.schemas import FAPreProcessorSchema, PydanticBaseModel
from lib.utils import hsash, types_

SchemaType = TypeVar("SchemaType", bound=PydanticBaseModel)


class FAPreProcessor(ABC, Generic[SchemaType]):
    """A preprocessor to prepare data for a model."""

    __PREFIX = "[FAPreProcessor] -"

    name: str
    uid: str | None = None
    params: SchemaType

    data: DataFrame

    bin_base_path = Path(os.getenv("BIN_PATH", "./bin")) / "pre_processors"

    def __init__(self, name: str = "") -> None:
        self.name = name or self.__class__.__name__

    @abstractmethod
    def run(self, data: DataFrame, params: SchemaType) -> DataFrame:
        """Run the preprocessor."""
        raise NotImplementedError

    def store(
        self,
        data: DataFrame,
        params: SchemaType | None,
    ) -> FAPreProcessorSchema | None:
        """Store the preprocessor in the database."""
        self.set_params(params)
        self.generate_hash(data)

        entry = db.PreProcessorTable.find_by_uid(types_.nn(self.uid))
        return entry or db.PreProcessorTable.insert(self.get_entry(), self.uid)

    def get_entry(self) -> FAPreProcessorSchema:
        """Return the entry for the preprocessor."""
        return FAPreProcessorSchema(
            uid=self.uid,
            name=self.name,
            params=self.params.model_dump(),
            data_hash=self.data_hash,
        )

    def generate_hash(self, data: Any) -> None:
        """Hash info and store it."""
        self.data_hash = hsash.hsh(data)
        self.uid = hsash.hsh(self.get_entry())

    def set_params(self, params: SchemaType | None) -> None:
        """Set the parameters for the preprocessor."""
        if not params:
            return

        if not hasattr(self, "params"):
            self.params = params
            return

        default_ = self.params.model_dump() if hasattr(self, "params") else {}
        runtime_ = params.model_dump()

        for key, value in runtime_.items():
            if key in default_ and type(value) is type(default_[key]):
                setattr(self.params, key, value)
