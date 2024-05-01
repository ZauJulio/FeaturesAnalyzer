import abc
from typing import Generic, Never, TypeVar

from interfaces import GenericWidget
from interfaces.application import ApplicationAbc
from lib.state_manager import State


class ControllerAbc(Generic[GenericWidget]):
    """Abstract controller class."""

    state: State
    widget: GenericWidget
    application: ApplicationAbc

    def __init__(
        self,
        application: ApplicationAbc,
        widget: GenericWidget,
        module_name: str,
        state: State,
    ) -> None:
        self.application = application
        self.widget = widget
        self.module_name = module_name
        self.state = state

        self._connect_signals()

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


GenericController = TypeVar("GenericController", bound=ControllerAbc)
