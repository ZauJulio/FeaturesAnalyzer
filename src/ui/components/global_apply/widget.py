from gi.repository import Gtk

from lib.utils import ui


class GlobalApplyWidget(Gtk.Button):
    """Global Apply Button."""

    def __init__(self) -> None:
        super().__init__(
            label="Apply",
            name="global-apply",
            width_request=30,
            height_request=30,
            margin_left=10,
            margin_right=10,
        )

        ui.load_styles(styles=__file__)
        ui.pointer_cursor(self)
