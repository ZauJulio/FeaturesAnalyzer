from gi.repository import Gtk

from lib.utils.ui import load_styles
from ui.components.shared import SideBarItem


class ImportSettingsWidget(SideBarItem):
    """Import settings."""

    selected_file: str
    selected_url: str

    file_radio: Gtk.RadioButton
    file_chooser: Gtk.FileChooserButton

    url_radio: Gtk.RadioButton
    url_entry: Gtk.Entry

    enter_box: Gtk.Box
    data_id_entry: Gtk.Entry

    def __init__(self) -> None:
        super().__init__(label="ImportSettings: Load Data")

        self.__load_layout()
        load_styles(styles=__file__)

    def __load_layout(self) -> None:
        """Load layout to the sidebar item."""
        # Main container
        self._container = Gtk.Box(
            name="import_settings_container",
            orientation=Gtk.Orientation.VERTICAL,
        )
        self.pack_start(self._container, expand=True, fill=True, padding=0)

        # Options container
        self.__setup_options_container()

        # Data entry box
        self.__setup_data_entry_box()

        # Data ID container
        self.__setup_data_id_container()

    def __setup_options_container(self) -> None:
        """Setup the options container with radio buttons."""
        options_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        options_container.set_name("options_container")
        options_container.set_halign(Gtk.Align.CENTER)
        options_container.set_spacing(50)
        self._container.add(options_container)

        # Label
        label = Gtk.Label(label="From:", name="from_label")
        options_container.add(label)

        # File radio button
        self.file_radio = Gtk.RadioButton.new_with_label(None, "File")
        self.file_radio.set_name("file_radio")
        self.file_radio.set_active(True)
        options_container.add(self.file_radio)

        # URL radio button
        self.url_radio = Gtk.RadioButton.new_with_label_from_widget(
            self.file_radio,
            "URL",
        )
        self.url_radio.set_name("url_radio")
        self.url_radio.set_active(False)
        options_container.add(self.url_radio)

    def __setup_data_entry_box(self) -> None:
        """Setup the data entry box for file chooser and URL entry."""
        self.enter_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.enter_box.set_name("enter_box")
        self.enter_box.set_spacing(15)
        self.enter_box.add(Gtk.Label(label="Enter:"))
        self._container.add(self.enter_box)

        # File chooser
        self.file_chooser = Gtk.FileChooserButton.new(
            "Select a file",
            Gtk.FileChooserAction.OPEN,
        )
        self.file_chooser.set_property("expand", True)
        self.file_chooser.set_name("file_chooser")
        self.file_chooser.set_current_folder("~/")
        self.enter_box.add(self.file_chooser)

        # URL entry
        self.url_entry = Gtk.Entry()
        self.url_entry.set_property("expand", True)
        self.url_entry.set_name("url_entry")
        self.url_entry.set_placeholder_text("Enter a URL")

    def __setup_data_id_container(self) -> None:
        """Setup the container for the data ID entry."""
        h_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        h_box.set_name("data_id_container")
        h_box.set_spacing(10)

        # Data ID label
        data_id_label = Gtk.Label(label="Data ID:")
        h_box.add(data_id_label)

        # Data ID entry
        self.data_id_entry = Gtk.Entry()
        self.data_id_entry.set_property("expand", True)
        self.data_id_entry.set_name("data_id_entry")
        self.data_id_entry.set_placeholder_text("Enter a data ID")
        h_box.add(self.data_id_entry)

        self._container.add(h_box)
