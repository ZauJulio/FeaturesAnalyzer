import threading
import time
from typing import Callable, List

import gi
import numpy as np

gi.require_version("Gtk", "3.0")
gi.require_version("GdkPixbuf", "2.0")

from gi.repository import GdkPixbuf, Gio, Gtk

from lib.utils.alias import at
from ui.components.graph_box import GraphBox
from ui.screens.app_window import ApplicationWindow


class FeaturesAnalyzer(Gtk.Application):
    """The main application class."""

    icon = GdkPixbuf.Pixbuf.new_from_file_at_size(at("@icon/app.png"), 64, 64)
    window: Gtk.Window = None

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
        Gtk.AboutDialog(
            logo=self.icon,
            transient_for=self.props.active_window,
            modal=True,
            program_name="FeaturesAnalyzer",
            version="0.1.0",
            authors=["Zaú Júlio"],
            copyright="© 2024 Zaú Júlio",
        ).present()

    def do_activate(self, *_, **__):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.window = self.window or ApplicationWindow(application=self)
        self.window.display()

        threading.Thread(
            target=self.update_graph, args=(self.window.graph,), daemon=True
        ).start()

    def update_graph(self, graph: GraphBox):
        """Update the graph with random data."""
        x = np.arange(0, 10, 0.1)
        y = np.sin(x)

        while True:
            # if the window is closed, stop the thread
            if not self.window.is_visible():
                break

            x = np.append(x, x[-1] + 0.1)
            y = np.append(y, np.sin(x[-1]))

            graph.plot(x, y)
            time.sleep(0.03)
