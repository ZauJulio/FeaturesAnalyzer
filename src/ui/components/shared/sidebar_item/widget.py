from collections.abc import Callable

from gi.repository import Gtk

from lib.utils.ui import load_styles


class SideBarItemHeader(Gtk.HBox):
    """Sidebar item header."""

    def __init__(self, label: str) -> None:
        super().__init__()

        self.__load_layout(label)

    def __load_layout(self, label: str) -> None:
        """Load layout to the sidebar item."""
        grid = Gtk.Grid()
        grid.set_name("header_grid")
        grid.set_hexpand(True)
        self.add(grid)

        self.label = Gtk.Label(label=label)
        self.label.set_name("header_label")
        self.label.set_halign(Gtk.Align.START)
        self.label.set_valign(Gtk.Align.CENTER)
        self.label.set_hexpand(True)
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_margin_start(10)
        grid.attach(self.label, 0, 0, 1, 1)

        self.status_button = Gtk.Button()
        self.status_button.set_name("status_button")
        self.status_button.set_property("visible", False)
        self.status_button.set_relief(Gtk.ReliefStyle.NONE)
        self.status_button.set_size_request(30, 30)
        self.status_button.set_tooltip_text("Status")
        grid.attach(self.status_button, 1, 0, 1, 1)


class SideBarItem(Gtk.Box):
    """Sidebar item."""

    head_bar: SideBarItemHeader
    notebook_item: Gtk.Notebook

    def __init__(self, label: str) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        self.set_property("expand", True)

        self.__load_layout(label)
        load_styles(styles=__file__)

    def __load_layout(self, label: str) -> None:
        """Load layout to the sidebar item."""
        self.set_name("notebook_container")

        self.head_bar = SideBarItemHeader(label=label)
        self.pack_start(self.head_bar, expand=False, fill=True, padding=0)

        self.notebook_item = Gtk.Notebook()
        self.notebook_item.set_name("notebook_item")
        self.pack_start(self.notebook_item, expand=True, fill=True, padding=0)

        # DND
        self.notebook_item.set_group_name(label)
        self.notebook_item.set_property("enable-popup", True)

    def add_tab(self, label: str, content: Gtk.Widget) -> None:
        """Add a tab to the notebook."""
        self.notebook_item.append_page(content, Gtk.Label(label=label))
        # DND
        self.notebook_item.set_tab_detachable(content, detachable=True)

    def handle_status(self, callback: Callable) -> None:
        """Handle the status button."""
        self.head_bar.status_button.connect("clicked", callback)

    def on_module_change(self) -> None:
        """Update the status button."""
        self.head_bar.status_button.set_property("visible", True)
        self.head_bar.status_button.set_tooltip_text("Apply")
        self.head_bar.status_button.set_label("✅")

    def on_module_updating(self) -> None:
        """Update the status button."""
        self.head_bar.status_button.set_property("visible", True)
        self.head_bar.status_button.set_tooltip_text("Cancel")
        self.head_bar.status_button.set_label("❌")

    def hide_module_status(self) -> None:
        """Update the status button."""
        self.head_bar.status_button.set_property("visible", False)

    def on_module_error(self) -> None:
        """Update the status button."""
        self.head_bar.status_button.set_property("visible", True)
        self.head_bar.status_button.set_tooltip_text("Error")
        self.head_bar.status_button.set_label("❗")
