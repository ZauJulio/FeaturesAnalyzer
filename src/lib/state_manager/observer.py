from abc import abstractmethod
from collections.abc import Callable, Generator
from contextlib import contextmanager
from copy import deepcopy
from typing import (
    Any,
    ClassVar,
    Literal,
    Never,
)

Callback = Callable[[Any, Any], None]
StateStatus = Literal["idle", "committing", "error"]
RootSubscriber = Literal["on_commit", "on_untrack"]


class Observer:
    """Mutable Observer."""

    _status: StateStatus = "idle"
    _tracked: bool = True
    _keys: ClassVar[set[str]] = set()
    _excluded_keys: ClassVar[set[str]] = {
        "_tracked",
        "_status",
        "on_commit",
        "on_untrack",
    }

    _subscribers: ClassVar[dict[str, list[Callback]]] = {}
    _root_subscribers: ClassVar[dict[RootSubscriber, list[Callback]]] = {}

    def __init__(self, annotations: set[str]) -> None:
        _init = {
            "_keys": annotations,
            "_subscribers": {},
            "_root_subscribers": {"on_commit": [], "on_untrack": []},
        }

        for key in annotations:
            _init[key] = None
            _init["_subscribers"][key] = []

        self.__dict__.update({**self.__dict__, **_init})

    @property
    def status(self) -> StateStatus:
        """Get immutable status."""
        return self._status

    @property
    def tracked(self) -> bool:
        """Get immutable track status."""
        return self._tracked

    def untrack(self) -> None:
        """Untrack the state."""
        self.__dict__["_tracked"] = False
        self._notify("on_untrack")

    def track(self) -> None:
        """Track the state."""
        self.__dict__["_tracked"] = True
        self.__dict__["_status"] = "idle"

    @abstractmethod
    def _get_untracked(self) -> Never:
        """Get the untracked state."""
        raise NotImplementedError

    @abstractmethod
    def _get_tracked(self) -> Never:
        """Get the tracked state."""
        raise NotImplementedError

    @abstractmethod
    def _track_changes(self, key: str, value: object) -> Never:
        """Update the state."""
        raise NotImplementedError

    def _validate_keys(self, key: str | list[str]) -> None:
        """Validate the key."""

        def validate(key: str) -> None:
            if not key.startswith("_") and key not in self._keys:
                msg = f"Invalid key: {key}"
                raise KeyError(msg)

        if isinstance(key, list):
            for k in key:
                validate(k)
        else:
            validate(key)

    def on_change(self, key: RootSubscriber | str, callback: Callback) -> None:
        """Add a subscriber to a key in the state."""
        if key in self._root_subscribers:
            self._root_subscribers[key].append(callback)
        elif key in self._keys:
            self._validate_keys(key)
            self._subscribers[key].append(callback)
        else:
            msg = f"Invalid key: {key}"
            raise KeyError(msg)

    def _notify(self, key: str, value: object | None = None) -> None:
        """Notify subscribers of a change."""
        listeners = []

        if key in self._subscribers:
            listeners = self._subscribers[key]
        elif key in self._root_subscribers:
            listeners = self._root_subscribers[key]
        else:
            msg = f"Invalid key: {key}"
            raise KeyError(msg)

        if listeners and len(listeners) > 0:
            if key == "on_commit":
                _prev = self._get_tracked()
                _next = self._get_untracked()
            else:
                _prev = self._get_untracked()
                _next = deepcopy(_prev)

                if value:
                    _next.__dict__[key] = value

            for listener in listeners:
                listener(_prev, _next)

    @contextmanager
    def __on_commit(self) -> Generator[None, None, None]:
        """Context manager for committing changes."""
        self.__dict__["_status"] = "committing"
        self._notify("on_commit")

        yield

        self.track()
        self.__dict__["_status"] = "idle"

    def commit(self) -> None:
        """Commit the untracked state."""
        with self.__on_commit():
            untracked = self._get_untracked()

            for key in self._keys:
                self._track_changes(key, getattr(untracked, key))
