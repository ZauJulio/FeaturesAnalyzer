from gi.repository import Gtk

from lib.utils import ui
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
        ui.load_styles(styles=__file__)

    def __load_layout(self) -> None:
        """Load layout to the sidebar item."""
        # Main container
        self._container = Gtk.VBox(name="import_settings_container", spacing=10)
        self.pack_start(self._container, expand=True, fill=True, padding=0)

        # Options container
        self.__setup_options_container()

        # Data entry box
        self.__setup_data_entry_box()

        # Data ID container
        self.__setup_data_id_container()

    def __setup_options_container(self) -> None:
        """Setup the options container with radio buttons."""
        options_box = Gtk.HBox(name="options_container")
        options_box.set_halign(Gtk.Align.CENTER)
        options_box.set_spacing(50)

        # File radio button
        self.file_radio = Gtk.RadioButton.new_with_label(None, "File")
        self.file_radio.set_name("file_radio")
        self.file_radio.set_active(True)

        # URL radio button
        self.url_radio = Gtk.RadioButton.new_with_label_from_widget(
            self.file_radio,
            "URL",
        )
        self.url_radio.set_name("url_radio")
        self.url_radio.set_active(False)

        options_box.add(Gtk.Label(label="From:", name="from_label"))
        options_box.add(self.file_radio)
        options_box.add(self.url_radio)

        self._container.add(options_box)

    def __setup_data_entry_box(self) -> None:
        """Setup the data entry box for file chooser and URL entry."""
        # File chooser
        self.file_chooser = Gtk.FileChooserButton.new(
            "Select a file",
            Gtk.FileChooserAction.OPEN,
        )
        self.file_chooser.set_hexpand(True)
        self.file_chooser.set_size_request(156, 30)
        self.file_chooser.set_name("file_chooser")
        self.file_chooser.set_current_folder("~/")

        # URL entry
        self.url_entry = Gtk.Entry(name="url_entry", expand=True)
        self.url_entry.set_placeholder_text("Enter a URL")

        self.enter_box = Gtk.HBox(name="enter_box", spacing=10)
        self.enter_box.add(Gtk.Label(label="Enter:", halign=Gtk.Align.START))
        self.enter_box.add(self.file_chooser)

        self._container.add(self.enter_box)

    def __setup_data_id_container(self) -> None:
        """Setup the container for the data ID entry."""
        # Data ID entry
        self.data_id_entry = Gtk.Entry(name="data_id_entry", expand=True)
        self.data_id_entry.set_placeholder_text("Enter a data ID")

        data_id_box = Gtk.HBox(name="data_id_container", spacing=10)
        data_id_box.add(Gtk.Label(label="Data ID:", halign=Gtk.Align.START))
        data_id_box.add(self.data_id_entry)

        self._container.add(data_id_box)
