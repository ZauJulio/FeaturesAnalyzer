from gi.repository import Gtk

from lib.utils import ui
from ui.components.shared import SideBarItem


class KMeansSolverWidget(SideBarItem):
    """KMeans Solver settings."""

    n_clusters: str
    max_iter: str

    def __init__(self) -> None:
        super().__init__(label="KMeans Solver")

        self.__load_layout()
        ui.load_styles(styles=__file__)

    def __load_layout(self) -> None:
        """Load layout to the sidebar item."""
        # Nº Cluster
        self.n_cluster_entry = Gtk.Entry(name="n_cluster_entry", expand=True, text="1")

        n_cluster_box = Gtk.HBox(name="n_cluster_box", spacing=10)
        n_cluster_box.add(Gtk.Label(label="Nº Cluster:", halign=Gtk.Align.START))
        n_cluster_box.add(self.n_cluster_entry)
        ##################################################################

        # Max Iter
        self.max_iter_entry = Gtk.Entry(name="max_iter_entry", expand=True, text="100")

        max_iter_box = Gtk.HBox(name="max_iter_box", spacing=10)
        max_iter_box.add(Gtk.Label(label="Max Iter:", halign=Gtk.Align.START))
        max_iter_box.add(self.max_iter_entry)
        ##################################################################

        # Main container
        self._container = Gtk.VBox(name="kmeans_solver_container", spacing=10)
        self._container.add(n_cluster_box)
        self._container.add(max_iter_box)

        self.pack_start(self._container, expand=True, fill=True, padding=0)
