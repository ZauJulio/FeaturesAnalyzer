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

        self.state.on_change(
            "selected_file",
            lambda _, next_: self.on_select_file(None, next_),
        )

    def on_select_file(self, _: None, next_: ImportSettingsState) -> None:
        """Select file."""
        # Get filename from path
        filename = next_.selected_file.split("/")[-1].split(".")[0]

        self.state.data_id = filename
        self.controller.widget.data_id_entry.set_text(filename)
