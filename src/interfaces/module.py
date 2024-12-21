from typing import Generic, TypeVar

from interfaces import GenericController, StateGeneric
from lib.utils import types


class FAModule(Generic[GenericController, StateGeneric]):
    """Abstract module class."""

    name: str
    controller: GenericController

    def __init__(self, controller: GenericController) -> None:
        self.controller = controller

    def get_widget(self):  # noqa: ANN201
        """Return the module widget."""
        return self.controller.widget

    def show(self) -> None:
        """Show the module."""
        self.controller.show()

    def hide(self) -> None:
        """Hide the module."""
        self.controller.hide()

    def reset(self) -> None:
        """Reset the module."""
        self.controller.reset()

    def load(self, state) -> None:  # noqa: ANN001
        """Load the module state."""
        self.controller.load(state)

    @property
    def state(self) -> StateGeneric:
        """Return the module state."""
        return self.controller.state


FAMetaCheckModule = types.MetaCheckGenerator(FAModule)
GenericModule = TypeVar("GenericModule", bound=FAModule)
