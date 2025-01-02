from gi.repository import Gtk

from lib.utils import ui
from ui.components.shared import SideBarItem


class MLPSolverWidget(SideBarItem):
    """MLP Solver settings."""

    hidden_layer_sizes: str
    activation: str
    solver: str
    max_iter: str

    def __init__(self) -> None:
        super().__init__(label="MLP Solver")

        self.__load_layout()
        ui.load_styles(styles=__file__)

    def __load_layout(self) -> None:
        """Load layout to the sidebar item."""
        # Hidden Layer Sizes
        self.hidden_layer_sizes_entry = Gtk.Entry(
            name="hidden_layer_sizes_entry",
            expand=True,
            text="100",
        )

        hidden_layer_sizes_box = Gtk.HBox(name="hidden_layer_sizes_box", spacing=10)
        hidden_layer_sizes_box.add(
            Gtk.Label(label="Hidden Layer Sizes:", halign=Gtk.Align.START),
        )
        hidden_layer_sizes_box.add(self.hidden_layer_sizes_entry)
        ##################################################################

        # Activation
        self.activation_combo = Gtk.ComboBoxText(name="activation_combo", expand=True)
        for option in ["identity", "logistic", "tanh", "relu"]:
            self.activation_combo.append_text(option)
        self.activation_combo.set_active(3)  # Default to "relu"

        activation_box = Gtk.HBox(name="activation_box", spacing=10)
        activation_box.add(Gtk.Label(label="Activation:", halign=Gtk.Align.START))
        activation_box.add(self.activation_combo)
        ##################################################################

        # Solver
        self.solver_combo = Gtk.ComboBoxText(name="solver_combo", expand=True)
        for option in ["lbfgs", "sgd", "adam"]:
            self.solver_combo.append_text(option)
        self.solver_combo.set_active(2)  # Default to "adam"

        solver_box = Gtk.HBox(name="solver_box", spacing=10)
        solver_box.add(Gtk.Label(label="Solver:", halign=Gtk.Align.START))
        solver_box.add(self.solver_combo)
        ##################################################################

        # Max Iter
        self.max_iter_entry = Gtk.Entry(name="max_iter_entry", expand=True, text="200")

        max_iter_box = Gtk.HBox(name="max_iter_box", spacing=10)
        max_iter_box.add(Gtk.Label(label="Max Iter:", halign=Gtk.Align.START))
        max_iter_box.add(self.max_iter_entry)
        ##################################################################

        # Main container
        self._container = Gtk.VBox(name="mlp_solver_container", spacing=10)
        self._container.add(hidden_layer_sizes_box)
        self._container.add(activation_box)
        self._container.add(solver_box)
        self._container.add(max_iter_box)

        self.pack_start(self._container, expand=True, fill=True, padding=0)
