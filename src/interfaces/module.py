from typing import TYPE_CHECKING, Generic, TypeVar

from gi.repository import Gtk

from interfaces import GenericController, GenericState
from lib.utils import types_

if TYPE_CHECKING:
    from app import FeaturesAnalyzer


class FAModule(Generic[GenericController, GenericState]):
    """Abstract module class."""

    name: str
    app: "FeaturesAnalyzer"
    controller: GenericController

    def __init__(self, app: "FeaturesAnalyzer", controller: GenericController) -> None:
        self.app = app
        self.controller = controller

        self.subscribe()

    def subscribe(self) -> None:
        """Load the module subscribers."""

    @property
    def widget(self) -> Gtk.Widget:
        """Return the module widget."""
        return self.controller.widget

    @property
    def state(self) -> GenericState:
        """Return the module state."""
        return self.controller.state

    def show(self) -> None:
        """Show the module."""
        self.controller.show()

    def hide(self) -> None:
        """Hide the module."""
        self.controller.hide()

    def reset(self) -> None:
        """Reset the module."""
        self.state.reset()
        self.controller.reset()

    def load(self, state: GenericState) -> None:
        """Load the module state."""
        self.controller.load(state)


FAMetaCheckModule = types_.MetaCheckBuilder(FAModule)
GenericModule = TypeVar("GenericModule", bound=FAModule)
