from urllib.parse import urlparse

from context.states import ImportSettingsState
from gi.repository import Gtk
from interfaces.application import ApplicationAbc
from interfaces.controller import ControllerAbc
from lib.utils import types
from ui.components.sidebar.import_settings.widget import ImportSettingsWidget


@types.property_meta(ControllerAbc)
class ImportSettingsController(ControllerAbc[ImportSettingsWidget]):
    """Import controller."""

    state: ImportSettingsState
    widget: ImportSettingsWidget
    application: ApplicationAbc

    def __handle_dialog(self, text: str, buttons: Gtk.ButtonsType) -> None:
        Gtk.MessageDialog(
            transient_for=self.application.window,
            message_type=Gtk.MessageType.INFO,
            text=text,
            buttons=buttons,
        )

    def _connect_signals(self) -> None:
        """Connect signals to the widget."""
        self.widget.file_radio.connect("toggled", self.__on_file_radio_toggled)
        self.widget.url_radio.connect("toggled", self.__on_url_radio_toggled)

        self.widget.file_chooser.connect("file-set", self.__on_file_chooser_file_set)
        self.widget.url_entry.connect("changed", self.__on_url_entry_changed)

        self.widget.data_id_entry.connect("changed", self.__on_data_id_entry_changed)

    def __on_file_radio_toggled(self, widget: Gtk.RadioButton) -> None:
        """File radio button toggled."""
        if widget.get_active():
            self.widget.url_entry.hide()
            self.widget.file_chooser.show()

    def __on_url_radio_toggled(self, widget: Gtk.RadioButton) -> None:
        """URL radio button toggled."""
        if widget.get_active():
            try:
                children = list(self.widget.enter_box.get_children())

                if children.index(self.widget.url_entry):
                    pass
            except ValueError:
                self.widget.enter_box.add(self.widget.url_entry)

            self.widget.file_chooser.hide()
            self.widget.url_entry.show()

    def __on_file_chooser_file_set(self, widget: Gtk.FileChooserButton) -> None:
        """File chooser file set."""
        self.state.selected_file = widget.get_filename() or ""

        self.__handle_dialog(
            text=f"Selected file: {self.state.selected_file}",
            buttons=Gtk.ButtonsType.OK,
        )

    def __on_url_entry_changed(self, widget: Gtk.Entry) -> None:
        """URL entry changed."""
        result = urlparse(str(widget.get_text()))

        if all([result.scheme, result.netloc, result.path]):
            self.__handle_dialog(text="✅", buttons=Gtk.ButtonsType.OK)

            self.widget.url_entry.set_tooltip_text("Valid URL")
            self.widget.url_entry.set_icon_from_icon_name(
                Gtk.EntryIconPosition.SECONDARY,
                "dialog-ok",
            )
        else:
            self.widget.url_entry.set_tooltip_text("Invalid URL")
            self.widget.url_entry.set_icon_from_icon_name(
                Gtk.EntryIconPosition.SECONDARY,
                "dialog-error",
            )

    def __on_data_id_entry_changed(self, widget: Gtk.Entry) -> None:
        """DataID entry changed."""
        self.state.data_id = str(widget.get_text())

        widget.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name="dialog-ok" if self.state.data_id else "dialog-error",
        )

    def reset(self) -> None:
        """Reset the import settings."""
        self.state.reset()

        self.widget.file_radio.set_active(True)
        self.widget.url_entry.set_text("")
        self.widget.data_id_entry.set_text("")

    def load(self, value: ImportSettingsState) -> None:
        """Load the import settings."""
        self.state.reset()

        self.state.selected_file = value.selected_file or ""
        self.state.selected_url = value.selected_url or ""
        self.state.data_id = value.data_id or ""

        if self.state.selected_file:
            self.widget.file_radio.set_active(True)
            self.widget.file_chooser.set_filename(self.state.selected_file)
        elif self.state.selected_url:
            self.widget.url_radio.set_active(True)
            self.widget.url_entry.set_text(self.state.selected_url)

        self.widget.data_id_entry.set_text(self.state.data_id)
