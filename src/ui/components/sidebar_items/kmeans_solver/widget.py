from gi.repository import Gtk

from lib.utils.ui import load_styles
from ui.components.shared import SideBarItem


class KMeansSolverWidget(SideBarItem):
    """KMeans Solver settings."""

    n_clusters: str
    max_iter: str

    def __init__(self) -> None:
        super().__init__(label="KMeans Solver")

        self.__load_layout()
        load_styles(styles=__file__)

    def __load_layout(self) -> None:
        """Load layout to the sidebar item."""
        # Nº Cluster
        n_cluster_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        n_cluster_box.set_name("n_cluster_box")
        n_cluster_box.set_spacing(10)

        self.n_cluster_entry = Gtk.Entry()
        self.n_cluster_entry.set_property("expand", True)
        self.n_cluster_entry.set_name("n_cluster_entry")
        self.n_cluster_entry.set_text("1")

        n_cluster_box.add(Gtk.Label(label="Nº Cluster:"))
        n_cluster_box.add(self.n_cluster_entry)
        ##################################################################

        # Max Iter
        max_iter_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        max_iter_box.set_name("max_iter_box")
        max_iter_box.set_spacing(10)

        self.max_iter_entry = Gtk.Entry()
        self.max_iter_entry.set_property("expand", True)
        self.max_iter_entry.set_name("max_iter_entry")
        self.max_iter_entry.set_text("100")

        max_iter_box.add(Gtk.Label(label="Max Iter:"))
        max_iter_box.add(self.max_iter_entry)
        ##################################################################

        # Main container
        self._container = Gtk.VBox(name="kmeans_solver_container")
        self.pack_start(self._container, expand=True, fill=True, padding=0)
        self._container.add(n_cluster_box)
        self._container.add(max_iter_box)
