import abc
from typing import Any, Generic, Never, TypeVar

from gi.repository import Gtk

from interfaces import StateGeneric
from lib.utils import types


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
    def _connect_signals(self) -> Never:
        """Connect signals to the widget."""
        raise NotImplementedError

    @abc.abstractmethod
    def reset(self) -> Never:
        """Reset the controller."""
        raise NotImplementedError

    @abc.abstractmethod
    def load(self, state) -> Never:  # noqa: ANN001
        """Load the controller state."""
        raise NotImplementedError

    def show(self) -> None:
        """Show the widget."""
        self.widget.show()

    def hide(self) -> None:
        """Hide the widget."""
        self.widget.hide()


FAMetaCheckController = types.MetaCheckGenerator(FAController)
GenericController = TypeVar("GenericController", bound=FAController)
