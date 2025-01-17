from typing import Any, cast

from gi.repository import Gtk

from interfaces import FAController, FAMetaCheckController

from . import MLPSolverState, MLPSolverWidget


@FAMetaCheckController
class MLPSolverController(FAController[MLPSolverState]):
    """MLP Solver controller."""

    state: MLPSolverState
    widget: MLPSolverWidget = MLPSolverWidget()

    def __init__(self, state: MLPSolverState) -> None:
        self.state = state

        self._connect_signals()

        # Load the initial state
        self.load(self.state)

        if (
            self.state.max_iter
            or self.state.hidden_layer_sizes
            or self.state.activation
            or self.state.solver
        ):
            self.widget.on_module_change()

    def _connect_signals(self) -> None:
        """Connect signals to the widget."""
        # Handle status and commit interface
        self.widget.max_iter_entry.connect("changed", self.__on_max_iter_changed)
        self.widget.hidden_layer_sizes_entry.connect(
            "changed",
            self.__on_hidden_layer_sizes_changed,
        )
        self.widget.activation_combo.connect("changed", self.__on_activation_changed)
        self.widget.solver_combo.connect("changed", self.__on_solver_changed)

    def __on_max_iter_changed(self, widget: Gtk.Entry) -> None:
        """Max Iter entry changed."""
        text = widget.get_text()
        if not text.isdigit() or int(text) < 1:
            widget.set_icon_from_icon_name(
                icon_pos=Gtk.EntryIconPosition.SECONDARY,
                icon_name="dialog-error",
            )
            return

        self.state.max_iter = int(text)
        widget.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name="dialog-ok",
        )

    def __on_hidden_layer_sizes_changed(self, widget: Gtk.Entry) -> None:
        """Hidden Layer Sizes entry changed."""
        text = widget.get_text()
        try:
            self.state.hidden_layer_sizes = tuple(map(int, text.split(",")))
            widget.set_icon_from_icon_name(
                icon_pos=Gtk.EntryIconPosition.SECONDARY,
                icon_name="dialog-ok",
            )
        except ValueError:
            widget.set_icon_from_icon_name(
                icon_pos=Gtk.EntryIconPosition.SECONDARY,
                icon_name="dialog-error",
            )

    def __on_activation_changed(self, widget: Gtk.ComboBoxText) -> None:
        """Activation function changed."""
        self.state.activation = cast("Any", widget.get_active_text())

    def __on_solver_changed(self, widget: Gtk.ComboBoxText) -> None:
        """Solver changed."""
        self.state.solver = cast("Any", widget.get_active_text())

    def reset(self) -> None:
        """Reset state."""
        self.widget.max_iter_entry.set_text("200")
        self.widget.hidden_layer_sizes_entry.set_text("100")
        self.widget.activation_combo.set_active(3)  # Default to "relu"
        self.widget.solver_combo.set_active(2)  # Default to "adam"

    def load(self, value: MLPSolverState) -> None:
        """Load state."""
        self.state.max_iter = value.max_iter or 200
        self.state.hidden_layer_sizes = value.hidden_layer_sizes or (100,)
        self.state.activation = value.activation or "relu"
        self.state.solver = value.solver or "adam"

        self.widget.max_iter_entry.set_text(str(self.state.max_iter))
        self.widget.hidden_layer_sizes_entry.set_text(
            ",".join(map(str, self.state.hidden_layer_sizes)),
        )

        self.widget.activation_combo.set_active_id(self.state.activation or "relu")
        self.widget.solver_combo.set_active_id(self.state.solver or "adam")
