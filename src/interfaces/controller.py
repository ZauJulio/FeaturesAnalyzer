import abc
from typing import Generic, TypeVar

from gi.repository import Gtk

from interfaces import GenericState
from lib.utils import types_


class FAController(Generic[GenericState]):
    """Abstract controller class."""

    state: GenericState
    widget: Gtk.Widget

    def __init__(self, state: GenericState) -> None:
        self.state = state

        self._connect_signals()

    def show(self) -> None:
        """Show the widget."""
        self.widget.show()

    def hide(self) -> None:
        """Hide the widget."""
        self.widget.hide()

    @abc.abstractmethod
    def _connect_signals(self) -> None:
        """Connect signals to the widget."""
        raise NotImplementedError

    @abc.abstractmethod
    def reset(self) -> None:
        """Reset the controller."""
        raise NotImplementedError

    @abc.abstractmethod
    def load(self, value: GenericState) -> None:
        """Load the controller state."""
        raise NotImplementedError


FAMetaCheckController = types_.MetaCheckBuilder(FAController)
GenericController = TypeVar("GenericController", bound=FAController)
