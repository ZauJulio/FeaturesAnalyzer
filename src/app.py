import threading
import time
from collections.abc import Callable

import gi
import numpy as np

gi.require_version("Gtk", "3.0")
gi.require_version("GdkPixbuf", "2.0")

from context import Store
from gi.repository import GdkPixbuf, Gio, Gtk
from interfaces.application import ApplicationAbc
from lib.utils import alias, types
from ui.components import GraphBox
from ui.screens import ApplicationWindow


@types.property_meta(ApplicationAbc)
class FeaturesAnalyzer(ApplicationAbc):
    """The main application class."""

    store: Store = Store()
    window: ApplicationWindow
    icon: GdkPixbuf.Pixbuf = types.nn(
        GdkPixbuf.Pixbuf.new_from_file_at_size(alias.at("@icon/app.png"), 64, 64),
    )

    def __init__(self) -> None:
        super().__init__(
            application_id="zaujulio.research.FeaturesAnalyzer",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

        self.create_actions("quit", lambda *_: self.quit(), ["<primary>q"])
        self.create_actions("about", lambda *_: self.on_about_action(), ["<primary>a"])

    def create_actions(
        self,
        name: str,
        callback: Callable,
        accel: list[str] = [],
    ) -> None:
        """Create and add a Gio.SimpleAction to the app."""
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)

        self.add_action(action)
        self.set_accels_for_action(f"app.{name}", accel)

    def on_about_action(self) -> None:
        """Call the app.about action."""
        Gtk.AboutDialog(
            logo=self.icon,
            transient_for=self.props.active_window,
            modal=True,
            program_name="FeaturesAnalyzer",
            version="0.1.0",
            authors=["Zaú Júlio"],
            copyright="© 2024 Zaú Júlio",
        ).present()

    def do_activate(self, *_, **__) -> None:  # noqa: ANN002, ANN003
        """Call when the application is activated."""
        if not hasattr(self, "window"):
            self.window = ApplicationWindow(application=self)

        self.window.display()

        threading.Thread(
            target=self.update_graph,
            args=(self.window.graph,),
            daemon=True,
        ).start()

    def update_graph(self, graph: GraphBox) -> None:
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
