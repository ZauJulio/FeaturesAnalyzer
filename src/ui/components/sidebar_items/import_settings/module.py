from typing import TYPE_CHECKING

from interfaces import FAMetaCheckModule, FAModule

from . import ImportSettingsController, ImportSettingsState

if TYPE_CHECKING:
    from app import FeaturesAnalyzer


@FAMetaCheckModule
class ImportSettingsModule(FAModule[ImportSettingsController, ImportSettingsState]):
    """Import settings module."""

    name: str = "ImportSettings"
    app: "FeaturesAnalyzer"
    controller: ImportSettingsController

    def __init__(self, app: "FeaturesAnalyzer", state: ImportSettingsState) -> None:
        super().__init__(
            app=app,
            controller=ImportSettingsController(state),
        )

    def subscribe(self) -> None:
        """Load the module subscribers."""
        # On track changes, update the module
        # show button to commit changes
        self.controller.widget.handle_status(state=self.state)

        with self.state as state:
            state.on_change(
                "on_untrack",
                lambda *_: self.controller.widget.on_module_change(),
            )

            state.on_change(
                "selected_file",
                lambda _, next_: self.on_select_file(None, next_),
            )

            state.on_change(
                "on_commit",
                lambda *_: state.handle_001_load_data(self.app),
            )

            state.on_change(
                "on_commit",
                lambda *_: state.handle_002_on_data_update(self.app),
            )

            state.on_change("on_commit", lambda *_: self.app.store.dump())

    def on_select_file(self, _: None, next_: ImportSettingsState) -> None:
        """Select file."""
        # Get filename from path
        filename = next_.selected_file.split("/")[-1].split(".")[0]

        self.state.data_id = filename
        self.controller.widget.data_id_entry.set_text(filename)
