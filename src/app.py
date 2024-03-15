import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gio, GdkPixbuf


class FeaturesAnalyzer(Gtk.Application):
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

    def do_activate(self):
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
