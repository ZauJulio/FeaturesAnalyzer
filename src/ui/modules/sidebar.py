from typing import TYPE_CHECKING, TypedDict

from gi.repository import Gtk

from lib.utils import ui
from ui.components.global_apply import GlobalApplyWidget
from ui.components.sidebar_items import (
    ImportSettingsModule,
    KMeansSolverModule,
    MLPSolverModule,
)


class SettingsModule(TypedDict):
    """Settings module."""

    ImportSettings: ImportSettingsModule
    KMeansSolver: KMeansSolverModule
    MLPSolver: MLPSolverModule


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

        def subscribe_mlp_solver() -> None:
            """Subscribe to the MLP Solver."""
            with self.settings["MLPSolver"].state as state:
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
        subscribe_mlp_solver()

    def __load_modules(self) -> None:
        """Load modules to the sidebar."""
        state = self.app.store.state

        self.settings: SettingsModule = {
            "ImportSettings": ImportSettingsModule(state=state.ImportSettings),
            "KMeansSolver": KMeansSolverModule(state=state.KMeansSolver),
            "MLPSolver": MLPSolverModule(state=state.MLPSolver),
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

        self.__load_global_apply()

    def __load_global_apply(self) -> None:
        """Load the global apply widget."""
        if TYPE_CHECKING:
            from lib.state_manager.state import FAState
            from ui.components.shared.sidebar_item import SideBarItem

        def on_click() -> None:
            """On click event."""
            for setting in self.settings:
                widget: SideBarItem = self.settings[setting].controller.widget
                state: FAState = self.settings[setting].controller.state

                state.commit()
                widget.hide_module_status()

        self.__global_apply = GlobalApplyWidget()
        self.__global_apply.connect("clicked", lambda _: on_click())
        self.__scroll_container.pack_end(
            child=self.__global_apply,
            expand=False,
            fill=False,
            padding=10,
        )

        for setting in self.settings:
            state: FAState = self.settings[setting].controller.state

            state.on_change("on_untrack", lambda *_: self.__global_apply.show())
            state.on_change("on_commit", lambda *_: self.__global_apply.hide())
