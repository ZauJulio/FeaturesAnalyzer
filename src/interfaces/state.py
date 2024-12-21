from typing import TypeVar

from lib.state_manager import State

StateGeneric = TypeVar("StateGeneric", bound=State)
