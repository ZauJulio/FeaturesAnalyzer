from gi.repository import Gtk

from interfaces import FAController, FAMetaCheckController

from . import KMeansSolverState, KMeansSolverWidget


@FAMetaCheckController
class KMeansSolverController(FAController[KMeansSolverState]):
    """KMeans Solver controller."""

    state: KMeansSolverState
    widget: KMeansSolverWidget

    def __init__(self, state: KMeansSolverState) -> None:
        super().__init__(state=state, widget=KMeansSolverWidget())

    def _connect_signals(self) -> None:
        """Connect signals to the widget."""
        # Handle status and commit interface
        self.widget.handle_status(state=self.state)

        self.widget.max_iter_entry.connect("changed", self.__on_data_iter_entry_changed)
        self.widget.n_cluster_entry.connect(
            "changed",
            self.__on_data_n_cluster_entry_changed,
        )

    def __on_data_iter_entry_changed(self, widget: Gtk.Entry) -> None:
        """Max Iter entry changed."""
        self.state.max_iter = int(widget.get_text())

        if self.state.max_iter < 0:
            self.state.max_iter = 0
            self.widget.max_iter_entry.set_text("0")

        widget.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name="dialog-ok" if self.state.max_iter else "dialog-error",
        )

    def __on_data_n_cluster_entry_changed(self, widget: Gtk.Entry) -> None:
        """N Cluster entry changed."""
        text = widget.get_text()

        if not text.isdigit() or text.startswith("0"):
            widget.set_text(text[:-1])
            return

        self.state.n_clusters = int(widget.get_text())

        if self.state.n_clusters < 0:
            self.state.n_clusters = 0
            self.widget.n_cluster_entry.set_text("0")

        widget.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name="dialog-ok" if self.state.n_clusters else "dialog-error",
        )

    def reset(self) -> None:
        """Reset state."""
        self.state.reset()

        self.widget.max_iter_entry.set_text("100")
        self.widget.n_cluster_entry.set_text("1")

    def load(self, value: KMeansSolverState) -> None:
        """Load state."""
        self.state.reset()

        self.state.max_iter = value.max_iter or 100
        self.state.n_clusters = value.n_clusters or 1

        self.widget.max_iter_entry.set_text(str(self.state.max_iter))
        self.widget.n_cluster_entry.set_text(str(self.state.n_clusters))
