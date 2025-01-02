from os import path

from gi.repository import Gdk, Gtk

from . import types_


def load_styles(source: str | None = None, styles: str | None = None) -> None:
    """
    Load styles for the widget.

    Parameters
    ----------
    source : str, optional
        The source file path, by default None
    styles : str, optional
        The styles file path, by default None

    """
    resource_path = path.dirname(types_.nn(source or styles))

    if source:
        filename = path.basename(source).replace(".py", ".css")  # noqa: PTH119
        styles_path = f"{resource_path}/{filename}"
    elif styles:
        styles_path = f"{resource_path}/styles.css"
    else:
        return

    screen = types_.nn(Gdk.Screen.get_default())
    priority = Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION

    provider = Gtk.CssProvider()
    provider.load_from_path(styles_path)

    Gtk.StyleContext().add_provider_for_screen(screen, provider, priority)


def pointer_cursor(widget: Gtk.Widget) -> None:
    """Change cursor to a hand pointer when hovering."""

    def on_hover_enter(widget: Gtk.Widget, _: Gdk.Event) -> None:
        """Change cursor to a hand pointer when hovering."""
        window = widget.get_window()
        if window:
            cursor = Gdk.Cursor.new_from_name(window.get_display(), "pointer")
            window.set_cursor(cursor)

    def on_hover_leave(widget: Gtk.Widget, _: Gdk.Event) -> None:
        """Reset cursor to default when not hovering."""
        window = widget.get_window()
        if window:
            window.set_cursor(None)

    # Enable pointer events
    widget.add_events(
        Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK,
    )

    # Connect hover signals
    widget.connect("enter-notify-event", on_hover_enter)
    widget.connect("leave-notify-event", on_hover_leave)
