from collections.abc import Callable
from typing import Any, ClassVar

import seaborn as sns
from gi.repository import Gtk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure

plt.style.use("ggplot")
sns.set_style("whitegrid")
plt.ion()


class GraphTab(Gtk.Box):
    """A tab to display a single graph."""

    def __init__(self) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas)

        self.pack_start(child=self.canvas, expand=True, fill=True, padding=0)
        self.pack_start(child=self.toolbar, expand=False, fill=False, padding=0)

        self.set_size_request(400, 300)

    def plot(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Plot data on the graph."""
        self.ax.clear()
        self.ax.plot(*args, **kwargs)
        self.canvas.draw()

    def seaborn_plot(self, sns_plot_func: Callable, *args: Any, **kwargs: Any) -> None:
        """
        Render a Seaborn plot on the graph.

        Parameters
        ----------
        sns_plot_func: Callable
            The Seaborn plotting function (e.g., sns.lineplot, sns.pairplot).
        *args: Any
            Positional arguments for the Seaborn function.
        **kwargs: Any
            Keyword arguments for the Seaborn function.

        """
        self.figure.clf()

        if sns_plot_func in {sns.pairplot, sns.jointplot}:
            sns_fig = sns_plot_func(*args, **kwargs)

            if hasattr(sns_fig, "fig"):
                sns_fig = sns_fig.fig

            self.canvas = FigureCanvas(sns_fig)
            self.toolbar = NavigationToolbar(self.canvas)

            for child in self.get_children():
                self.remove(child)

            self.pack_start(self.canvas, expand=True, fill=True, padding=0)
            self.pack_start(self.toolbar, expand=False, fill=False, padding=0)

            plt.close(sns_fig)
            self.canvas.show()
            self.toolbar.show()
        else:
            self.ax = self.figure.add_subplot(111)
            sns_plot_func(*args, ax=self.ax, **kwargs)
            self.canvas.draw()

        self.show_all()


class GraphNotebook(Gtk.Notebook):
    """A notebook to manage multiple graph tabs."""

    tabs: ClassVar[dict[str, GraphTab]] = {}

    def __init__(self) -> None:
        super().__init__()

        self.set_tab_pos(Gtk.PositionType.TOP)
        self.add_tab("__default__", "Graph")

    def add_tab(self, key: str, title: str) -> GraphTab:
        """Add a new graph tab with the given key and title."""
        if key in self.tabs:
            msg = f"A tab with key '{key}' already exists."
            raise KeyError(msg)

        if len(self.tabs) == 1 and "__default__" in self.tabs:
            self.remove_tab("__default__")

        self.tabs[key] = GraphTab()

        close_button = Gtk.Button(label="✖")
        close_button.set_relief(Gtk.ReliefStyle.NONE)
        close_button.set_focus_on_click(False)
        close_button.connect("clicked", lambda _: self.remove_tab(key))

        tab_label = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        tab_label.pack_start(Gtk.Label(label=title), expand=True, fill=True, padding=0)
        tab_label.pack_start(close_button, expand=False, fill=False, padding=0)
        tab_label.show_all()

        self.append_page(self.tabs[key], tab_label)
        self.show_all()
        return self.tabs[key]

    def get_tab(self, key: str) -> GraphTab:
        """Retrieve a graph tab by its key."""
        if key not in self.tabs:
            msg = f"No tab with key '{key}' found."
            raise KeyError(msg)

        return self.tabs[key]

    def remove_tab(self, key: str) -> None:
        """Remove a graph tab by its key."""
        if key not in self.tabs:
            msg = f"No tab with key '{key}' found."
            raise KeyError(msg)

        page = self.tabs.pop(key)
        page_num = self.page_num(page)
        if page_num != -1:
            self.remove_page(page_num)
