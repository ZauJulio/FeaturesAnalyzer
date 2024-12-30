from typing import TYPE_CHECKING, TypedDict

from gi.repository import Gtk

from lib.utils import ui
from ui.components.sidebar_items import ImportSettingsModule, KMeansSolverModule


class SettingsModule(TypedDict):
    """Settings module."""

    ImportSettings: ImportSettingsModule
    KMeansSolver: KMeansSolverModule


class SideBar(Gtk.ScrolledWindow):
    """Sidebar options."""

    if TYPE_CHECKING:
        from app import FeaturesAnalyzer

    __side_bar: Gtk.Viewport
    __scroll_container: Gtk.VBox

    app: "FeaturesAnalyzer"

    def __init__(self, app: "FeaturesAnalyzer") -> None:
        super().__init__(min_content_width=350)

        self.app = app

        ui.load_styles(source=__file__)

        self.__load_modules()
        self.__load_layout()
        self.__subscribe()

    def __subscribe(self) -> None:
        """Subscribe to the sidebar."""

        def subscribe_import_settings() -> None:
            """Subscribe to the import settings."""
            with self.settings["ImportSettings"].state as state:
                state.on_change(
                    "on_commit",
                    lambda *_: state.handle_001_load_data(self.app),
                )

                state.on_change(
                    "on_commit",
                    lambda *_: state.handle_002_on_data_update(self.app),
                )

                state.on_change(
                    "on_commit",
                    lambda *_: self.app.store.dump(),
                )

        def subscribe_kmeans_solver() -> None:
            """Subscribe to the KMeans Solver."""
            with self.settings["KMeansSolver"].state as state:
                state.on_change(
                    "on_commit",
                    lambda *_: state.handle_001_on_params_update(self.app),
                )

                state.on_change(
                    "on_commit",
                    lambda *_: self.app.store.dump(),
                )

        subscribe_import_settings()
        subscribe_kmeans_solver()

    def __load_modules(self) -> None:
        """Load modules to the sidebar."""
        state = self.app.store.state

        self.settings: SettingsModule = {
            "ImportSettings": ImportSettingsModule(state=state.ImportSettings),
            "KMeansSolver": KMeansSolverModule(state=state.KMeansSolver),
        }

    def __load_layout(self) -> None:
        """Load layout to the sidebar."""
        label = Gtk.Label(label="Settings", name="sidebar-label")
        self.__scroll_container = Gtk.VBox(valign=Gtk.Align.START)
        self.__scroll_container.pack_start(label, expand=True, fill=True, padding=0)

        self.__side_bar = Gtk.Viewport(hscroll_policy=Gtk.ScrollablePolicy.NATURAL)
        self.__side_bar.add(self.__scroll_container)
        self.add(self.__side_bar)

        for setting in self.settings:
            self.__scroll_container.pack_start(
                child=self.settings[setting].controller.widget,
                expand=False,
                fill=False,
                padding=0,
            )
