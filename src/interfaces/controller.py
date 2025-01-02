import abc
from typing import Any, Generic, TypeVar

from gi.repository import Gtk

from interfaces import StateGeneric
from lib.utils import types_


class FAController(Generic[StateGeneric]):
    """Abstract controller class."""

    state: StateGeneric
    widget: Any

    def __init__(self, widget: Any, state: StateGeneric) -> None:
        self.state = state
        self.widget = widget

        self._connect_signals()

    @staticmethod
    def _handle_dialog(text: str, buttons: Gtk.ButtonsType) -> None:
        Gtk.MessageDialog(
            message_type=Gtk.MessageType.INFO,
            text=text,
            buttons=buttons,
        )

    @abc.abstractmethod
    def _connect_signals(self) -> None:
        """Connect signals to the widget."""
        raise NotImplementedError

    def _load_initial_state(self) -> None:
        """Load the initial state."""

    @abc.abstractmethod
    def reset(self) -> None:
        """Reset the controller."""
        raise NotImplementedError

    @abc.abstractmethod
    def load(self, state) -> None:  # noqa: ANN001
        """Load the controller state."""
        raise NotImplementedError

    def show(self) -> None:
        """Show the widget."""
        self.widget.show()

    def hide(self) -> None:
        """Hide the widget."""
        self.widget.hide()


FAMetaCheckController = types_.MetaCheckBuilder(FAController)
GenericController = TypeVar("GenericController", bound=FAController)
