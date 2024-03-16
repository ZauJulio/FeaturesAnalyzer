import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from lib.utils.alias import at
from ui.components.graph_box import GraphBox


class ApplicationWindow(Gtk.ApplicationWindow):
    """Main application window"""

    builder = Gtk.Builder()
    builder.add_from_file(at("@layout/AppLayout"))

    # Containers
    container: Gtk.Box = builder.get_object("AppLayout")
    graph_container: Gtk.Box = builder.get_object("GraphContainer")

    # Components
    graph: GraphBox = None

    def __init__(self, application: Gtk.Application):
        super().__init__(application=application)

        self.set_title("Features Analyzer")
        self.set_default_size(800, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon(application.icon)

        self.connect("destroy", Gtk.main_quit)

    def load_widgets(self):
        """Load widgets to the window."""
        self.add(self.container)

        self.graph = GraphBox()
        self.graph_container.add(self.graph)

    def display(self):
        """Show all widgets in the window."""
        self.load_widgets()
        self.show_all()
