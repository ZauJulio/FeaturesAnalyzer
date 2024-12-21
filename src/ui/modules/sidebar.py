from typing import TYPE_CHECKING, Any, TypedDict

from gi.repository import Gtk

from ui.components.sidebar_items import ImportSettingsModule


class SettingsModule(TypedDict):
    """Settings module."""

    ImportSettings: ImportSettingsModule


class SideBar(Gtk.ScrolledWindow):
    """Sidebar options."""

    if TYPE_CHECKING:
        from app import FeaturesAnalyzer

    __side_bar: Gtk.Viewport
    __scroll_container: Gtk.VBox

    app: "FeaturesAnalyzer"

    def __init__(self, app: "FeaturesAnalyzer") -> None:
        super().__init__()

        self.app = app

        self.set_min_content_width(350)

        self.__load_layout()
        self.__subscribe()

    def __load_layout(self) -> None:
        """Load layout to the sidebar."""
        self.__scroll_container = Gtk.VBox(
            valign=Gtk.Align.START,
            orientation=Gtk.Orientation.VERTICAL,
        )

        self.__side_bar = Gtk.Viewport(hscroll_policy=Gtk.ScrollablePolicy.NATURAL)
        self.__side_bar.add(self.__scroll_container)
        self.add(self.__side_bar)

        state = self.app.store.state
        self.settings: SettingsModule = {
            "ImportSettings": ImportSettingsModule(state=state.ImportSettings),
        }

        for setting in self.settings:
            self.__scroll_container.pack_start(
                child=self.settings[setting].controller.widget,
                expand=False,
                fill=False,
                padding=0,
            )

    def __subscribe(self) -> None:
        """Subscribe to the sidebar."""
        state = self.app.store.state.ImportSettings

        def on_data_update(*_: Any) -> None:
            """Update the graph."""
            data = self.app.store.state.data[state.data_id]

            x = data.iloc(0)
            y = data.iloc(1)

            self.app.window.graph.plot(x, y)

        def _update_data_store(*_: Any) -> None:
            import pandas as pd

            """Update the data store with the selected file or URL."""
            if state.data_id and (state.selected_file or state.selected_url):
                df: pd.DataFrame | None = None
                source = state.selected_file or state.selected_url

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
                    self.app.store.state.data[state.data_id] = df

        self.settings["ImportSettings"].state.on_change("on_commit", _update_data_store)
        self.settings["ImportSettings"].state.on_change("on_commit", on_data_update)
