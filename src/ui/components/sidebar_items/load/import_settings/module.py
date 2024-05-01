import pandas as pd
from context.states import ImportSettingsState
from interfaces.application import ApplicationAbc
from interfaces.module import ModuleAbc
from lib.utils import types

from .controller import ImportSettingsController
from .widget import ImportSettingsWidget


@types.property_meta(ModuleAbc)
class ImportSettingsModule(ModuleAbc[ImportSettingsController]):
    """Import settings module."""

    module_name: str = "ImportSettings"
    controller: ImportSettingsController
    state: ImportSettingsState

    def __init__(self, application: ApplicationAbc) -> None:
        self.state = application.store.state.ImportSettings

        super().__init__(
            application,
            controller=ImportSettingsController(
                application=application,
                widget=ImportSettingsWidget(application),
                module_name=self.module_name,
                state=self.state,
            ),
        )

        self.subscribe()

    def subscribe(self) -> None:
        """Load the module subscribers."""
        # On commit changes to the data store
        self.state.on_change(
            "on_commit",
            lambda _, _next: self._update_data_store(_next),
        )

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

    def _update_data_store(self, _next: ImportSettingsState) -> None:
        """Update the data store with the selected file or URL."""
        if _next.data_id and (_next.selected_file or _next.selected_url):
            df: pd.DataFrame | None = None
            source = _next.selected_file or _next.selected_url

            match source.split(".")[-1]:
                case "csv":
                    df = pd.read_csv(source)
                case "json":
                    df = pd.read_json(source)
                case "xlsx":
                    df = pd.read_excel(source)
                case _:
                    pass

            if df is not None:
                self.application.store.state.data[_next.data_id] = df
