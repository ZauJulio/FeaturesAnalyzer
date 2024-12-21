from typing import ClassVar

import pandas as pd

from context.states import ImportSettingsState
from lib.state_manager import State
from lib.utils.meta import SingletonMeta


class StateType(State):
    """Global application state."""

    data: ClassVar[dict[str, pd.DataFrame]]
    ImportSettings: ImportSettingsState


class Store(metaclass=SingletonMeta):
    """State class for storing global state."""

    __state = StateType(state={
        "data": {},
        "ImportSettings": ImportSettingsState(),
    })

    @property
    def state(self) -> StateType:
        """Return the state."""
        return self.__state

    # Create, dump and load by JSON
