from interfaces import FAMetaCheckModule, FAModule

from . import ImportSettingsController, ImportSettingsState


@FAMetaCheckModule
class ImportSettingsModule(FAModule[ImportSettingsController, ImportSettingsState]):
    """Import settings module."""

    name: str = "ImportSettings"
    controller: ImportSettingsController

    def __init__(self, state: ImportSettingsState) -> None:
        super().__init__(controller=ImportSettingsController(state))

        self.subscribe()

    def subscribe(self) -> None:
        """Load the module subscribers."""
        # On track changes, update the module
        # show button to commit changes
        self.state.on_change(
            "on_untrack",
            lambda *_: self.controller.widget.on_module_change(),
        )

        # Handle status changes, like committing or updating
        # show the status button to apply or cancel the changes
        self.controller.widget.handle_status(lambda *_: self._update_module_status())

    def _update_module_status(self) -> None:
        """Update the module status."""
        if not self.state.tracked:
            if self.state.status != "committing":
                self.controller.widget.on_module_updating()
                self.state.commit()
                self.controller.widget.hide_module_status()
            else:
                self.controller.widget.hide_module_status()
                self.state.reset()
