import abc
from collections.abc import Callable
from typing import Never

from gi.repository import GdkPixbuf, Gtk

from context.store import Store
from lib.utils import types_
from ui.screens import ApplicationWindow


class FAApplication(Gtk.Application):
    """Abstract application class."""

    store: Store
    window: ApplicationWindow

    icon: GdkPixbuf.Pixbuf

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


FAMetaCheckApplication = types_.MetaCheckBuilder(FAApplication)
