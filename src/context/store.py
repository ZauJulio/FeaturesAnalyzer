from typing import ClassVar, cast

import pandas as pd

from context.states import ImportSettingsState, KMeansSolverState, MLPSolverState
from lib.orm import db
from lib.state_manager import FAState
from lib.utils import SingletonMeta, logger

PREFIX = "[STORE] -"


class StateType(FAState):
    """Global application state."""

    data: ClassVar[dict[str, pd.DataFrame]]

    ImportSettings: ImportSettingsState
    KMeansSolver: KMeansSolverState
    MLPSolver: MLPSolverState


class Store(metaclass=SingletonMeta):
    """State class for storing global state."""

    __state = StateType(
        state={
            "data": {},
            "ImportSettings": ImportSettingsState(),
            "KMeansSolver": KMeansSolverState(),
            "MLPSolver": MLPSolverState(),
        },
    )

    def __init__(self) -> None:
        self.load()

    @property
    def state(self) -> StateType:
        """Return the state."""
        return self.__state

    def dump(self) -> None:
        """Dump state to json."""
        if db.SettingsTable.find_by_uid("root"):
            db.SettingsTable.remove(doc_ids=["root"])

        db.SettingsTable.insert(
            db.SettingsTable.schema(value=self.__state.serialize()),
            uid="root",
        )

        logger.info(f"{PREFIX} State dumped.")

    def load(self) -> None:
        """Load state from json."""
        state = db.SettingsTable.find_by_uid("root")

        if state:
            self.__state.load(state.value)

            for key in self.__state.__annotations__:
                if isinstance(self.__state[key], FAState):
                    cast("FAState", self.__state[key]).untrack()

            logger.info(f"{PREFIX} State loaded.")
