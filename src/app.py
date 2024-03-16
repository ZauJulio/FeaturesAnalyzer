import threading
import time
from typing import Callable, List
import numpy as np
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gio, GdkPixbuf
from ui.components.graph_box import GraphBox


class FeaturesAnalyzer(Gtk.Application):
    """The main application class."""

    app_icon = GdkPixbuf.Pixbuf.new_from_file_at_size("../assets/icons/app.png", 64, 64)

    builder: Gtk.Builder
    window: Gtk.Window
    graph: GraphBox

    def __init__(self):
        super().__init__(
            application_id="zaujulio.research.FeaturesAnalyzer",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

        self.create_actions("quit", lambda *_: self.quit(), ["<primary>q"])
        self.create_actions("about", lambda *_: self.on_about_action(), ["<primary>a"])

    def create_actions(self, name: str, callback: Callable, accel: List[str] = []):
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
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/views/windows/MainWindow.ui")
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("MainWindow")
        self.window.set_icon(self.app_icon)
        self.add_window(self.window)

        self.window.show_all()

        self.load_graph()

    def load_graph(self):
        """Load the graph on the main window."""
        self.graph = GraphBox()

        self.builder.get_object("graph_container").add(self.graph)
        self.graph.show_all()

        thread = threading.Thread(target=self.update_graph, args=(self.graph,))
        thread.start()

    def update_graph(self, graph: GraphBox):
        """Update the graph with random data."""
        x = np.arange(0, 10, 0.1)
        y = np.sin(x)

        while True:
            x = np.append(x, x[-1] + 0.1)
            y = np.append(y, np.sin(x[-1]))

            graph.plot(x, y)
            time.sleep(0.03)

            # if the window is closed, stop the thread
            if not self.window.is_visible():
                break
