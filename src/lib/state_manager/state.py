from collections.abc import Callable
from typing import Any, ClassVar, Literal, Self, cast, get_args

from lib.utils import logger

from . import FAObserver

Callback = Callable[[Any, Any], None]
StateStatus = Literal["idle", "committing", "error"]
RootSubscriber = Literal["on_commit", "on_untrack"]

PREFIX = "[State Manager] -"


class FAState(FAObserver):
    """State manager."""

    _state: ClassVar[dict[str, Any]] = {}
    _backup: Self

    def __init__(self, state: dict[str, Any] = {}) -> None:
        super().__init__(annotations=set(self.__annotations__.keys()))

        self.load(state)

    def __getitem__(self, key: str) -> object:
        """Get the value of a key from tracked state."""
        return self._state[key]

    def __setattr__(self, key, value) -> None:  # noqa: ANN001
        """Set the value of a key."""
        # Check if key is a member of the class
        self._validate_keys(key)

        # Get the expected type from annotations
        expected_type = self.__annotations__.get(key)

        if not expected_type:
            msg = f"Invalid key {key}"
            logger.error(f"{PREFIX} {msg}")
            raise KeyError(msg)

        # Handle Literal types
        if hasattr(expected_type, "__origin__") and expected_type.__origin__ is Literal:
            # Extract allowed values from Literal
            allowed_values = get_args(expected_type)
            if value not in allowed_values:
                msg = f"{PREFIX} Invalid value {value!r} for {key}, expected one of {allowed_values}"  # noqa: E501
                logger.error(msg)
                raise ValueError(msg)

        # Handle tuple[int, ...] check
        elif hasattr(expected_type, "__origin__") and expected_type.__origin__ is tuple:
            # Ensure the tuple is of type tuple[int, ...]
            if not all(isinstance(item, int) for item in value):
                msg = f"{PREFIX} Invalid type in tuple for {key}, expected all elements to be of type int"  # noqa: E501
                logger.error(msg)
                raise TypeError(msg)

        # Validate non-Literal types
        elif not isinstance(value, expected_type):
            msg = f"Invalid type {type(value)} for {key}, expected {expected_type}"
            raise TypeError(msg)

        # Notify subscribers
        if getattr(self, key, None) != value:
            self._notify(key, value)
            self.__dict__[key] = value

            self.untrack()

    def get_state(self):  # noqa: ANN201
        """Get the state."""
        return self._state

    def serialize(self) -> dict:
        """Recursively serialize state."""
        import pandas as pd

        def _serialize_value(value: Any) -> object:
            if isinstance(value, FAState):
                return value.serialize()

            if isinstance(value, dict):
                return {k: _serialize_value(v) for k, v in value.items()}

            if isinstance(value, list):
                return [_serialize_value(v) for v in value]

            if isinstance(value, pd.DataFrame):
                return None

            return value

        return {
            key: _serialize_value(value)
            for key, value in self._copy(cls=self).__dict__.items()
        }

    def _get_untracked(self) -> Self:
        """Get the untracked state."""
        return self._copy(self)

    def _get_tracked(self) -> Self:
        """Get the tracked state."""
        return self._copy(obj=self._state)

    def _track_changes(self, key: str, value: object) -> None:
        """Update the state."""
        self._state[key] = value

    def _copy(self, cls: Self | None = None, obj: dict[str, Any] | None = None) -> Self:
        """Copy the state to a new class object."""

        class SelfMask:
            _tracked: bool

            def __init__(
                self,
                cls: FAState | None = None,
                obj: dict[str, Any] | None = None,
                _tracked: bool = True,
            ) -> None:
                keys_ = None

                if cls:
                    keys_ = cls.__annotations__.keys()

                    def _get(key: str) -> object:
                        return getattr(cls, key)

                elif obj:
                    keys_ = obj.keys()

                    def _get(key: str) -> object:
                        return obj[key]

                else:
                    msg = "Invalid state"
                    raise ValueError(msg)

                self.__dict__ = {
                    **{key: _get(key) for key in keys_},
                    "_tracked": _tracked,
                }

        return cast("Self", SelfMask(cls, obj, self._tracked))

    def reset(self) -> None:
        """Reset the state to its initial values."""
        for k, v in self._state.items():
            # Reset by type
            value = None

            if isinstance(v, list):
                value = []
            elif isinstance(v, dict):
                value = {}
            elif isinstance(v, str):
                value = ""
            elif isinstance(v, int):
                value = 0
            elif isinstance(v, float):
                value = 0.0
            elif isinstance(v, bool):
                value = False

            self._state[k] = value
            self.__dict__[k] = value

        self.track()

    def load(self, value: dict[str, Any]) -> None:
        """Load a state from a dictionary, supporting nested FAState instances."""
        self._validate_keys(list(value.keys()))

        for k in self._keys:
            if isinstance(self._state.get(k), FAState):
                self._state[k].load(value[k])
            else:
                self._state[k] = value[k]
                self.__dict__[k] = value[k]

        self.track()

    def __enter__(self) -> Self:
        """Enter the context and backup the current state."""
        self.__dict__["_backup"] = self._copy(self)

        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        """Exit the context and restore the previous state if an exception occurs."""
        if exc_type is not None:
            # Restore the backup state in case of an exception
            self.load(self._backup.__dict__)

        del self._backup
