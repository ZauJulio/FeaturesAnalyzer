from typing import ClassVar

import pandas as pd

from context.states import ImportSettingsState, KMeansSolverState
from lib.state_manager import FAState
from lib.utils import SingletonMeta


class StateType(FAState):
    """Global application state."""

    data: ClassVar[dict[str, pd.DataFrame]]

    ImportSettings: ImportSettingsState
    KMeansSolver: KMeansSolverState


class Store(metaclass=SingletonMeta):
    """State class for storing global state."""

    __state = StateType(
        state={
            "data": {},
            "ImportSettings": ImportSettingsState(),
            "KMeansSolver": KMeansSolverState(),
        },
    )

    @property
    def state(self) -> StateType:
        """Return the state."""
        return self.__state

    # Create, dump and load by JSON
