from gi.repository import Gdk, Gtk

from lib.utils import alias, types_
from ui.modules import GraphNotebook, SideBar


class ApplicationWindow(Gtk.ApplicationWindow):
    """Main application window."""

    builder = Gtk.Builder()
    builder.add_from_file(alias.at("@layout/AppLayout"))

    # Containers
    container: Gtk.Box = types_.nn(builder.get_object("AppLayout"))
    side_bar_container: Gtk.Box = types_.nn(builder.get_object("SideBarContainer"))
    graph_container: Gtk.Box = types_.nn(builder.get_object("GraphContainer"))

    # Components
    graph: GraphNotebook
    side_bar: SideBar

    def __init__(self, application: types_.Any) -> None:
        super().__init__(application=application)

        self.set_title("Features Analyzer")
        self.set_default_size(800, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon(application.icon)

        self.connect("destroy", Gtk.main_quit)
        self.connect("key-press-event", self.on_key_press)

    def on_key_press(self, _: Gtk.Widget, event: Gdk.EventKey) -> None:  # noqa: PLR6301
        """Handle close key press events."""
        # Alt+F4
        if event.keyval == Gdk.KEY_F4 and (event.state & Gdk.ModifierType.MOD1_MASK):
            Gtk.main_quit()

    def load_widgets(self) -> None:
        """Load widgets to the window."""
        self.add(self.container)

        self.graph = GraphNotebook()
        self.graph_container.add(self.graph)

        self.side_bar = SideBar(app=types_.nn(self.get_application()))
        self.side_bar_container.add(self.side_bar)

    def display(self) -> None:
        """Show all widgets in the window."""
        self.load_widgets()
        self.show_all()
