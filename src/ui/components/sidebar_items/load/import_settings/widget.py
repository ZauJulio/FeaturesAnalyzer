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

    def __init__(self, application: object) -> None:
        super().__init__(application, "Load")

        self.__load_layout()
        load_styles(styles=__file__)

    def __load_layout(self) -> None:
        """Load layout to the sidebar item."""
        self.import_tab_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.import_tab_container.set_name("import_tab_container")
        self.add_tab("Import", self.import_tab_container)
        self.__load_import_tab()

        self.select_tab_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.select_tab_container.set_name("select_tab_container")
        self.add_tab("Select", self.select_tab_container)

    def __load_import_tab(self) -> None:
        """Load the import tab."""
        label = Gtk.Label(label="From:")
        label.set_name("from_label")
        self.import_tab_container.add(label)
        ##############################################################

        # Options container
        options_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        options_container.set_name("options_container")
        options_container.set_halign(Gtk.Align.CENTER)
        options_container.set_spacing(50)
        self.import_tab_container.add(options_container)

        # Radio Group
        #########
        # File option
        #########
        self.file_radio = Gtk.RadioButton.new_with_label(None, "File")
        self.file_radio.set_name("file_radio")
        self.file_radio.set_active(True)
        #########
        # URL option
        #########
        self.url_radio = Gtk.RadioButton.new_with_label_from_widget(
            self.file_radio,
            "URL",
        )
        self.url_radio.set_name("url_radio")
        self.url_radio.set_active(False)
        options_container.add(self.file_radio)
        options_container.add(self.url_radio)
        ##############################################################

        # Data Enter
        self.enter_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.enter_box.set_name("enter_box")
        self.enter_box.set_spacing(15)
        self.enter_box.add(Gtk.Label(label="Enter:"))
        self.import_tab_container.add(self.enter_box)
        #########
        # By file
        #########
        self.file_chooser = Gtk.FileChooserButton.new(
            "Select a file",
            Gtk.FileChooserAction.OPEN,
        )
        self.file_chooser.set_property("expand", True)
        self.file_chooser.set_name("file_chooser")
        self.file_chooser.set_current_folder("~/")
        self.enter_box.add(self.file_chooser)
        #########
        # By URL
        #########
        self.url_entry = Gtk.Entry()
        self.url_entry.set_property("expand", True)
        self.url_entry.set_name("url_entry")
        self.url_entry.set_placeholder_text("Enter a URL")
        ##############################################################

        # Data ID
        self.data_id_entry = Gtk.Entry()
        self.data_id_entry.set_property("expand", True)
        self.data_id_entry.set_name("data_id_entry")
        self.data_id_entry.set_placeholder_text("Enter a data ID")
        #########
        # Container
        #########
        h_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        h_box.set_name("data_id_container")
        h_box.set_spacing(10)
        h_box.add(Gtk.Label(label="Data ID:"))
        h_box.add(self.data_id_entry)
        self.import_tab_container.add(h_box)
        ##############################################################
