from os import path

from gi.repository import Gdk, Gtk

from . import types


def load_styles(source: str | None = None, styles: str | None = None) -> None:
    """Load styles for the widget."""
    resource_path = path.dirname(types.nn(source or styles))

    if source:
        filename = path.basename(source).replace(".py", ".css")  # noqa: PTH119
        styles_path = f"{resource_path}/{filename}"
    elif styles:
        styles_path = f"{resource_path}/styles.css"
    else:
        return

    screen = types.nn(Gdk.Screen.get_default())
    priority = Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION

    provider = Gtk.CssProvider()
    provider.load_from_path(styles_path)

    Gtk.StyleContext().add_provider_for_screen(screen, provider, priority)
