from typing import TypedDict

from gi.repository import Gtk
from interfaces.application import ApplicationAbc
from interfaces.module import ModuleAbc
from ui.components.sidebar_items.load.import_settings.module import ImportSettingsModule


class SettingsModule(TypedDict):
    """Settings module."""

    label: str
    module: ModuleAbc


class SideBar(Gtk.ScrolledWindow):
    """Sidebar options."""

    __side_bar: Gtk.Viewport
    __scroll_container: Gtk.VBox

    def __init__(self, application: ApplicationAbc) -> None:
        super().__init__()

        self.application = application
        self.set_min_content_width(350)
        self.__load_layout()

    def __load_layout(self) -> None:
        """Load layout to the sidebar."""
        self.__side_bar = Gtk.Viewport()
        self.__side_bar.set_hscroll_policy(Gtk.ScrollablePolicy.NATURAL)
        self.add(self.__side_bar)

        self.__scroll_container = Gtk.VBox(orientation=Gtk.Orientation.VERTICAL)
        self.__scroll_container.set_valign(Gtk.Align.START)
        self.__side_bar.add(self.__scroll_container)

        self.settings: list[SettingsModule] = [
            {
                "label": "ImportSettings",
                "module": ImportSettingsModule(application=self.application),
            },
        ]

        for setting in self.settings:
            self.__scroll_container.pack_start(
                child=setting["module"].get_widget(),
                expand=False,
                fill=False,
                padding=0,
            )
