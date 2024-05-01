from typing import Generic, TypeVar

from interfaces.application import ApplicationAbc
from interfaces.controller import GenericController


class ModuleAbc(Generic[GenericController]):
    """Abstract module class."""

    module_name: str
    controller: GenericController

    def __init__(
        self,
        application: ApplicationAbc,
        controller: GenericController,
    ) -> None:
        self.application = application
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

    def get_state(self):  # noqa: ANN201
        """Return the module state."""
        return self.controller.state

    @staticmethod
    def handle_module_apply() -> None:
        """Handle the module apply."""
        print("Module apply")  # noqa: T201


GenericModule = TypeVar("GenericModule", bound=ModuleAbc)
