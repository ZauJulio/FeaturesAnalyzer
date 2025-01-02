import os
from datetime import datetime
from pathlib import Path
from typing import Any, Generic, TypeVar

import numpy as np
import pandas as pd

from lib.model_manager import FAPreProcessor
from lib.orm import db
from lib.orm.schemas import FAModelSchema, PydanticBaseModel
from lib.utils import bin_, hsash, logger, time_

ParamsType = TypeVar("ParamsType", bound=PydanticBaseModel)
ModelType = TypeVar("ModelType")


class FAModelManager(Generic[ModelType, ParamsType]):
    """A manager for FA models."""

    __PREFIX = "[FAModelManager] -"
    file_name: str
    bin_base_path = Path(os.getenv("BIN_PATH", "./bin")) / "models"
    Path(bin_base_path).mkdir(parents=True, exist_ok=True)

    schema: type[ParamsType]
    method: ModelType

    # Model data
    uid: str | None = None
    name: str
    params: ParamsType
    pre_processors: list[str] = []

    def add_pre_processor(self, method: FAPreProcessor) -> None:
        """Add a preprocessor to the model."""
        if not hasattr(method, "uid") or not method.uid:
            msg = f"{self.__PREFIX} - Preprocessor must have a uid."
            logger.error(msg)
            raise ValueError(msg)

        if method.uid not in self.pre_processors:
            self.pre_processors.append(method.uid)

    def set_params(self, params: ParamsType | None) -> None:
        """Set the parameters for the method."""
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

    def store(
        self,
        data: pd.DataFrame | np.ndarray,
        params: ParamsType | None,
    ) -> tuple[FAModelSchema, Any | None] | None:
        """Store the model in the database."""
        self.set_params(params)
        self.generate_hash(data)

        if not self.uid:
            return None

        dt = datetime.now(tz=time_.tz).strftime("%Y-%m-%d_%H-%M-%S")
        self.file_name = f"{self.name}_{dt}_{self.uid}.pkl"
        self.file_name = self._find_bin_by_uid() or self.file_name

        entry = db.ModelTable.find_by_uid(self.uid)

        try:
            self.method = bin_.load(path=self.bin_base_path / self.file_name)

            if self.method and entry:
                logger.success(f"{self.__PREFIX} - Model loaded from {self.file_name}.")
                return entry, self.method

            if not entry:
                msg = (f"{self.__PREFIX} - Missing entry for {self.uid}.",)
                raise db.MissingDBEntryError(msg)  # noqa: TRY301
        except FileNotFoundError:
            logger.info(f"{self.__PREFIX} - Model binary not found.")

            if not entry:
                entry = db.ModelTable.insert(self.get_entry(), self.uid)

            return entry, None
        except db.MissingDBEntryError:
            logger.info(f"{self.__PREFIX} - Model entry not found.")

            entry = db.ModelTable.insert(self.get_entry(), self.uid)
            return entry, None
        except Exception as e:
            logger.error(f"{self.__PREFIX} - {e}")
            raise

    def get_entry(self) -> FAModelSchema:
        """Return the entry for the model."""
        if not hasattr(self, "name"):
            self.name = self.__class__.__name__

        return FAModelSchema(
            name=self.name,
            uid=self.uid or None,
            pre_processors=self.pre_processors,
            params=self.params.model_dump(),
            data_hash=self.data_hash,
        )

    def _find_bin_by_uid(self) -> str | None:
        """Find the binary file by uid."""
        if not self.uid:
            return None

        for file in self.bin_base_path.iterdir():
            if file.is_file() and self.uid in file.name:
                return file.name

        return None

    def loaded(self) -> bool:
        """Check if the model is loaded."""
        return hasattr(self, "method")

    def save(self) -> None:
        """Save the model binary."""
        if self.loaded():
            logger.info(f"{self.__PREFIX} - Saving model to {self.file_name}.")
            bin_.write(self.method, self.bin_base_path / self.file_name)

    def generate_hash(self, data: Any) -> None:
        """Hash info and store it."""
        self.data_hash = hsash.hsh(data)
        self.uid = hsash.hsh(self.get_entry())
