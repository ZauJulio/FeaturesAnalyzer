from gi.repository import Gtk
from interfaces.application import ApplicationAbc
from lib.utils import alias, types
from ui.components import GraphBox
from ui.components.sidebar.sidebar import SideBar


class ApplicationWindow(Gtk.ApplicationWindow):
    """Main application window."""

    builder = Gtk.Builder()
    builder.add_from_file(alias.at("@layout/AppLayout"))

    # Containers
    container: Gtk.Box = types.nn(builder.get_object("AppLayout"))
    side_bar_container: Gtk.Box = types.nn(builder.get_object("SideBarContainer"))
    graph_container: Gtk.Box = types.nn(builder.get_object("GraphContainer"))

    # Components
    graph: GraphBox
    side_bar: SideBar

    def __init__(self, application: ApplicationAbc) -> None:
        super().__init__(application=application)

        self.set_title("Features Analyzer")
        self.set_default_size(800, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon(application.icon)

        self.connect("destroy", Gtk.main_quit)

    def load_widgets(self) -> None:
        """Load widgets to the window."""
        self.add(self.container)

        self.graph = GraphBox()
        self.graph_container.add(self.graph)

        self.side_bar = SideBar(application=types.nn(self.get_application()))  # type: ignore  # noqa: PGH003
        self.side_bar_container.add(self.side_bar)

    def display(self) -> None:
        """Show all widgets in the window."""
        self.load_widgets()
        self.show_all()
