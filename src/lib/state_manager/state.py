from collections.abc import Callable
from typing import Any, ClassVar, Literal, Self, cast

from . import FAObserver

Callback = Callable[[Any, Any], None]
StateStatus = Literal["idle", "committing", "error"]
RootSubscriber = Literal["on_commit", "on_untrack"]


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
        # Check if key is member of the class
        self._validate_keys(key)

        # Validate type of value/annotation
        if value.__class__ is not self.__annotations__[key]:
            type_ = type(value)
            expected_ = self.__annotations__[key]

            msg = f"Invalid type {type_} for {key}, expected {expected_}"
            raise TypeError(msg)

        # Notify subscribers
        if getattr(self, key) != value:
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
