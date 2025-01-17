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

    def __load_modules(self) -> None:
        """Load modules to the sidebar."""
        state = self.app.store.state

        self.settings: SettingsModule = {
            "ImportSettings": ImportSettingsModule(
                app=self.app,
                state=state.ImportSettings,
            ),
            "KMeansSolver": KMeansSolverModule(
                app=self.app,
                state=state.KMeansSolver,
            ),
            "MLPSolver": MLPSolverModule(
                app=self.app,
                state=state.MLPSolver,
            ),
        }

    def __load_layout(self) -> None:
        """Load layout to the sidebar."""
        if TYPE_CHECKING:
            from lib.state_manager.state import FAState
            from ui.components.shared.sidebar_item import SideBarItem

        def on_click() -> None:
            """On click to apply all settings."""
            for setting in self.settings:
                widget: SideBarItem = self.settings[setting].widget
                state: FAState = self.settings[setting].state

                state.commit()
                widget.hide_module_status()

        self.__scroll_container = Gtk.VBox(valign=Gtk.Align.START)
        self.__scroll_container.pack_start(
            Gtk.Label(label="Settings", name="sidebar-label"),
            expand=True,
            fill=True,
            padding=0,
        )

        self.__side_bar = Gtk.Viewport(hscroll_policy=Gtk.ScrollablePolicy.NATURAL)
        self.__side_bar.add(self.__scroll_container)
        self.add(self.__side_bar)

        self.__global_apply = GlobalApplyWidget()
        self.__global_apply.connect("clicked", lambda _: on_click())

        for setting in self.settings:
            module = self.settings[setting]
            state: FAState = module.state

            self.__scroll_container.pack_start(
                child=module.widget,
                expand=False,
                fill=False,
                padding=0,
            )

            # Connect root signals
            state.on_change("on_untrack", lambda *_: self.__global_apply.show())
            state.on_change("on_commit", lambda *_: self.__global_apply.hide())

        self.__scroll_container.pack_end(
            child=self.__global_apply,
            expand=False,
            fill=False,
            padding=10,
        )
