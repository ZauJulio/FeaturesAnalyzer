import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class SideBar(Gtk.ScrolledWindow):
    """Sidebar options"""

    def __init__(self, application):
        super().__init__()

        self.application = application
        # Set min width
        self.set_min_content_width(350)
        self.load_layout()

    def load_layout(self):
        """Load layout to the sidebar."""
        self.side_bar = Gtk.Viewport()
        self.side_bar.set_hscroll_policy(Gtk.ScrollablePolicy.NATURAL)
        self.add(self.side_bar)

        self.scroll_container = Gtk.VBox(orientation=Gtk.Orientation.VERTICAL)
        self.side_bar.add(self.scroll_container)

        # Sidebar items
        self.preprocess_settings = PreprocessSettings(self.application)
        self.scroll_container.add(self.preprocess_settings)

        self.load_settings = LoadSettings(self.application)
        self.scroll_container.add(self.load_settings)


class SideBarItem(Gtk.Box):
    """Sidebar item"""

    application: any
    label: Gtk.Label
    notebook: Gtk.Notebook

    def __init__(self, application, label: str):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        self.application = application

        self.set_property("expand", True)

        self.load_layout(label)
        self.show_all()

    def load_layout(self, label: str):
        """Load layout to the sidebar item."""

        self.label = Gtk.Label(label)
        self.label.set_markup(f'<span weight="bold" size="large">{label}</span>')
        self.pack_start(self.label, expand=False, fill=False, padding=0)

        self.notebook = Gtk.Notebook()
        self.notebook.set_property("show-border", False)
        self.pack_start(self.notebook, expand=False, fill=False, padding=0)

    def add_tab(self, label: str, content: Gtk.Widget):
        """Add a tab to the notebook."""
        self.notebook.append_page(content, Gtk.Label(label))


class PreprocessSettings(SideBarItem):
    """Load settings"""

    def __init__(self, application):
        super().__init__(application, "Load")

        self._load_layout()

    def _load_layout(self):
        """Load layout to the sidebar item."""
        self.import_tab_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add_tab("Import", self.import_tab_container)

        self.select_tab_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add_tab("Select", self.select_tab_container)


class LoadSettings(SideBarItem):
    """Preprocess settings"""

    def __init__(self, application):
        super().__init__(application, "Preprocess")

        self._load_layout()

    def _load_layout(self):
        """Load layout to the sidebar item."""
        self.fill_tab_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add_tab("Fill", self.fill_tab_container)

        self.normalize_tab_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add_tab("Normalize", self.normalize_tab_container)

        self.discretize_tab_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add_tab("Discretize", self.discretize_tab_container)
