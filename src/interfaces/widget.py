from typing import TypeVar

from gi.repository import Gtk

GenericWidget = TypeVar("GenericWidget", bound=Gtk.Widget)
