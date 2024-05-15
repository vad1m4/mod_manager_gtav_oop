import tkinter as tk
from pathlib import Path

from mod_manager import config
from mod_manager.commands import (
    CopyCommand,
    DeleteAllCommand,
    DeleteCommand,
    EditCommand,
    ExportToFileCommand,
    ImportFromFileCommand,
    SaveAndCloseCommand,
    SubmitNameCommand,
    SubmitAllCommand,
)
from mod_manager.formatter import format_record
from mod_manager.components import ButtonsFrame, NameEntry, LinkEntry, RecordListFrame
from mod_manager.storage import JSONFileRecordStorage


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(background=config.GREY)
        self.title("Mod manager")
        self.resizable(False, False)
        self.iconphoto(True, tk.PhotoImage(file="images/icon.png"))
        self.grid_rowconfigure(1, uniform=1)

        self.storage = JSONFileRecordStorage(Path.cwd() / "history.json")

        self.record_list_frame = RecordListFrame(parent=self)
        self.buttons_frame = ButtonsFrame(parent=self)
        self.name_entry = NameEntry(parent=self)
        self.link_entry = LinkEntry(parent=self)
        self.name_entry.bind("<FocusIn>", self.on_entry_focus)
        self.link_entry.bind("<FocusIn>", self.on_entry_focus)

        self.restore_records()
        self.create_commands()

    def restore_records(self) -> None:
        for record in self.storage.read():
            name = record.get("name")
            self.record_list_frame.listbox.insert("end", name)

    def on_entry_focus(self, e) -> None:
        if self.name_entry.get() in ("Name cannot be empty!","Select one entry only!"):
            self.name_entry.delete(0, "end")
        if self.link_entry.get() == "Invalid link!":
            self.link_entry.delete(0, "end")

    def create_commands(self) -> None:
        record_list = self.record_list_frame.listbox

        delete_command = DeleteCommand(
            self,
            record_list,
            self.storage,
            self.name_entry,
            self.link_entry,
        )
        self.buttons_frame.delete_button.config(command=delete_command.execute)

        delete_all_command = DeleteAllCommand(
            self,
            record_list,
            self.storage,
            self.name_entry,
            self.link_entry,
        )
        self.buttons_frame.delete_all_button.config(command=delete_all_command.execute)

        edit_command = EditCommand(
            self,
            record_list,
            self.storage,
            self.name_entry,
            self.link_entry,
        )
        self.buttons_frame.edit_button.config(command=edit_command.execute)

        copy_command = CopyCommand(
            self,
            record_list,
            self.storage,
            self.name_entry,
            self.link_entry,
        )
        self.buttons_frame.copy_button.config(
            command=lambda: copy_command.execute(True, True)
        )

        self.bind("<Control-c>", lambda _: copy_command.execute())
        self.bind("<Control-x>", lambda _: copy_command.execute(False, True))

        export_to_file_command = ExportToFileCommand(
            self,
            record_list,
            self.storage,
            self.name_entry,
            self.link_entry,
        )
        self.buttons_frame.export_to_file_button.config(
            command=export_to_file_command.execute
        )

        import_from_file_command = ImportFromFileCommand(
            self,
            record_list,
            self.storage,
            self.name_entry,
            self.link_entry,
        )
        self.buttons_frame.import_from_file_button.config(
            command=import_from_file_command.execute
        )

        save_and_close_command = SaveAndCloseCommand(
            self,
            record_list,
            self.storage,
            self.name_entry,
            self.link_entry,
        )
        self.buttons_frame.save_and_close_button.config(
            command=save_and_close_command.execute
        )

        submit_name_command = SubmitNameCommand(
            self,
            record_list,
            self.storage,
            self.name_entry,
            self.link_entry,
        )
        submit_all_command = SubmitAllCommand(
            self,
            record_list,
            self.storage,
            self.name_entry,
            self.link_entry,
        )
        self.name_entry.bind("<Return>", lambda _: submit_name_command.execute())
        self.link_entry.bind("<Return>", lambda _: submit_all_command.execute())
