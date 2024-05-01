import abc
from collections.abc import Callable
from typing import Never

from context.store import Store
from gi.repository import GdkPixbuf, Gtk


class ApplicationAbc(Gtk.Application):
    """Abstract application class."""

    store: Store = Store()
    icon: GdkPixbuf.Pixbuf
    window: Gtk.ApplicationWindow

    @abc.abstractmethod
    def create_actions(
        self,
        name: str,
        callback: Callable,
        accel: list[str] = [],
    ) -> Never:
        """Create and add a Gio.SimpleAction to the app."""
        raise NotImplementedError

    @abc.abstractmethod
    def do_activate(self, *_, **__) -> Never:  # noqa: ANN002, ANN003
        """Called when the application is activated."""
        raise NotImplementedError
