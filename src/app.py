import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gio, GdkPixbuf
from src.ui.components.graph_box import GraphBox


class FeaturesAnalyzer(Gtk.Application):
    """The main application class."""

    window: Gtk.Window

    def __init__(self):
        super().__init__(
            application_id="zaujulio.research.FeaturesAnalyzer",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

        self.app_icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            "../assets/icons/app.png", 64, 64
        )

        self.create_actions("quit", lambda *_: self.quit(), ["<primary>q"])
        self.create_actions("about", lambda *_: self.on_about_action(), ["<primary>a"])

    def create_actions(self, name, callback, accel):
        """Create and add a Gio.SimpleAction to the app."""
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)

        self.add_action(action)
        self.set_accels_for_action(f"app.{name}", accel)

    def on_about_action(self, *_):
        """Callback for the app.about action."""
        about = Gtk.AboutDialog(
            logo=self.app_icon,
            transient_for=self.props.active_window,
            modal=True,
            program_name="FeaturesAnalyzer",
            version="0.1.0",
            authors=["Zaú Júlio"],
            copyright="© 2024 Zaú Júlio",
        )

        about.present()

    def do_activate(self, *_, **__):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        builder = Gtk.Builder()
        builder.add_from_file("ui/views/windows/MainWindow.ui")
        builder.connect_signals(self)

        self.window = builder.get_object("MainWindow")
        self.window.set_icon(self.app_icon)
        self.add_window(self.window)
        self.window.show_all()

        self.load_graph(builder)

    def load_graph(self, builder: Gtk.Builder):
        """Load the graph on the main window."""
        # Select graph_container as the graph container
        graph_container = builder.get_object("graph_container")

        # Create a GraphBox instance
        graph_box = GraphBox()
        graph_container.add(graph_box)
        graph_box.show_all()

        # plot some data
        graph_box.plot([1, 2, 3, 4], [1, 4, 9, 16])
