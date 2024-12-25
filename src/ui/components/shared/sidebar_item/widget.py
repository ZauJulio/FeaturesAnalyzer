from gi.repository import Gtk

from lib.state_manager import FAState
from lib.utils import ui


class SideBarItemHeader(Gtk.HBox):
    """Sidebar item header."""

    def __init__(self, label: str) -> None:
        super().__init__(name="head-bar")

        self.__load_layout(label)

    def __load_layout(self, label: str) -> None:
        """Load layout to the sidebar item."""
        grid = Gtk.Grid(name="header_grid", hexpand=True)
        self.add(grid)

        self.label = Gtk.Label(
            label=label,
            name="header_label",
            halign=Gtk.Align.START,
            valign=Gtk.Align.CENTER,
            hexpand=True,
            justify=Gtk.Justification.CENTER,
            margin_start=10,
        )

        self.status_button = Gtk.Button(
            name="status_button",
            visible=False,
            relief=Gtk.ReliefStyle.NONE,
            tooltip_text="Status",
            width_request=30,
            height_request=30,
        )

        grid.attach(self.label, 0, 0, 1, 1)
        grid.attach(self.status_button, 1, 0, 1, 1)


class SideBarItem(Gtk.Box):
    """Sidebar item."""

    head_bar: SideBarItemHeader
    notebook_item: Gtk.Notebook

    def __init__(self, label: str) -> None:
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            name="sidebar-item",
            expand=True,
            spacing=0,
        )

        self.__load_layout(label)
        ui.load_styles(styles=__file__)

    def __load_layout(self, label: str) -> None:
        """Load layout to the sidebar item."""
        self.head_bar = SideBarItemHeader(label=label)
        self.pack_start(self.head_bar, expand=False, fill=True, padding=0)

    def handle_status(self, state: FAState) -> None:
        """Handle the status button."""

        def on_any_change(state: FAState) -> None:
            """Update the module status."""
            # Handle status changes, like committing or updating
            # show the status button to apply or cancel the changes
            if not state.tracked:
                if state.status != "committing":
                    self.on_module_updating()
                    state.commit()
                    self.hide_module_status()
                else:
                    self.hide_module_status()
                    state.reset()

        self.head_bar.status_button.connect("clicked", lambda _: on_any_change(state))

    def on_module_change(self) -> None:
        """Update the status button."""
        self.show_module_status()
        self.head_bar.status_button.set_tooltip_text("Apply")
        self.head_bar.status_button.set_label("✅")

    def on_module_updating(self) -> None:
        """Update the status button."""
        self.show_module_status()

        self.head_bar.status_button.set_tooltip_text("Cancel")
        self.head_bar.status_button.set_label("❌")

    def hide_module_status(self) -> None:
        """Update the status button."""
        self.head_bar.status_button.set_property("opacity", 0)

    def show_module_status(self) -> None:
        """Update the status button."""
        self.head_bar.status_button.set_property("opacity", 1)

    def on_module_error(self) -> None:
        """Update the status button."""
        self.show_module_status()

        self.head_bar.status_button.set_tooltip_text("Error")
        self.head_bar.status_button.set_label("❗")
