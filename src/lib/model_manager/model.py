import os
from datetime import datetime
from pathlib import Path
from typing import Any, Generic, Self

import pandas as pd

from lib.orm import db
from lib.orm.schemas import FAModelSchema, SchemaType
from lib.utils import bin_, hsash, logger, time_


class FAModelManager(Generic[SchemaType]):
    """A manager for FA models."""

    __PREFIX = "[FAModelManager] -"
    bin_base_path = Path(os.getenv("BIN_PATH", "./bin")) / "models"

    data: pd.DataFrame

    schema: type[SchemaType]

    name: str
    params: SchemaType
    pre_processors: list[str]

    def set_params(self, params: SchemaType | None) -> None:
        """Set the parameters for the preprocessor."""
        if not params:
            return

        default_ = self.params.model_dump()
        runtime_ = params.model_dump()

        for key, value in runtime_.items():
            if type(value) is type(default_[key]):
                setattr(self.params, key, value)

    def __rewrite(self, instance: Self) -> None:
        """Rewrite the instance with the new one."""
        self.__class__ = instance.__class__
        self.__dict__.update(instance.__dict__)

    def store(
        self,
        data: pd.DataFrame,
        params: SchemaType | None,
    ) -> tuple[FAModelSchema, bool] | None:
        """Store the preprocessor in the database."""
        self.set_params(params)
        self.generate_hash(data)

        dt = datetime.now(tz=time_.tz).strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{self.name}_{dt}_{self.uid}.pkl"

        try:
            if not self.uid:
                return None

            entry = db.ModelTable.find_by_uid(self.uid)
            instance = bin_.load(path=self.bin_base_path / file_name)

            if instance and entry:
                self.__rewrite(instance)
                return entry, False

            if not entry:
                msg = (f"{self.__PREFIX} - Missing entry for {self.uid}.",)
                raise db.MissingDBEntryError(msg)  # noqa: TRY301
        except FileNotFoundError:
            entry = db.ModelTable.insert(self.get_entry(), self.uid)
            instance = bin_.write(self, self.bin_base_path / file_name)

            return entry, True
        except db.MissingDBEntryError:
            entry = db.ModelTable.insert(self.get_entry(), self.uid)
            instance = bin_.write(self, self.bin_base_path / file_name)

            return entry, True
        except Exception as e:
            logger.error(f"{self.__PREFIX} - {e}")
            raise

    def get_entry(self) -> FAModelSchema:
        """Return the entry for the model."""
        return FAModelSchema(
            name=self.name,
            uid=self.uid,
            pre_processors=self.pre_processors,
            params=self.params.model_dump(),
            data_hash=self.data_hash,
        )

    def generate_hash(self, data: Any) -> None:
        """Hash info and store it."""
        self.data_hash = hsash.hsh(data)
        self.model_hash = hsash.hsh(self.get_entry())

        self.uid = hsash.hsh(self.get_entry())
