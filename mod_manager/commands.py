import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from abc import ABC, abstractmethod
from mod_manager.exceptions import (
    EmptyNameError,
    InvalidLinkError,
    SelectError,
)
from mod_manager.validator import is_url_valid

from mod_manager.formatter import format_record
from mod_manager.storage import RecordStorage, PlainTextRecordStorage


class Command(ABC):
    def __init__(
        self,
        app: tk.Tk,
        record_list: tk.Listbox,
        storage: RecordStorage,
        name_entry: tk.Entry,
        link_entry: tk.Entry,
    ):
        self.app = app
        self.record_list = record_list
        self.storage = storage
        self.name_entry = name_entry
        self.link_entry = link_entry

    @abstractmethod
    def execute(self): ...


class DeleteCommand(Command):
    def execute(self):
        records_to_delete = self.record_list.curselection()
        self.storage.delete(records_to_delete)
        for item in reversed(records_to_delete):
            self.record_list.delete(item)


class DeleteAllCommand(Command):
    def execute(self):
        self.storage.write([])
        self.record_list.delete(0, "end")


class EditCommand(Command):
    def execute(self):
        try:
            if len(self.record_list.curselection()) > 1:
                raise SelectError("Select one entry only!")
            else:
                self.name_entry.delete(0, "end")
                name, link = format_record(
                    self.record_list.curselection()[0], self.storage
                )
                self.name_entry.insert(0, name)
                self.link_entry.insert(0, link)
                self.app.name_entry.focus()
                DeleteCommand.execute(self)
        except SelectError as e:
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, e)
            self.app.focus()


class CopyCommand(Command):
    def execute(self, addName: bool = True, addLink: bool = False):
        self.app.clipboard_clear()
        for index in self.record_list.curselection():
            name, link = format_record(index, self.storage)
            if addName:
                self.app.clipboard_append(f"{name}\n")
            if addLink:
                self.app.clipboard_append(f"{link}\n")
            self.app.update()


class ExportToFileCommand(Command):
    def execute(self):
        import time

        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"exports\modlist_{timestamp}.txt"

        with open(filename, "w") as file:
            for index, text in enumerate(self.record_list.get(0, "end")):
                name, link = format_record(index, self.storage)
                file.write(f"Name: {name}\n")
                if link:
                    file.write(f"Link: {link}\n")
                file.write("----\n")
        import subprocess
        from pathlib import Path

        subprocess.Popen(f'explorer /select,"{Path.cwd()}\{filename}"')


class ImportFromFileCommand(Command):
    def execute(self):
        self.textfile = filedialog.askopenfile(
            initialdir=f"{Path.cwd()}/exports",
            filetypes=(
                ("Text Files", "*.txt"),
                ("JSON Files", "*.json"),
                ("All files", "*.*"),
            ),
        )
        if ".txt" in self.textfile:
            txt = PlainTextRecordStorage(self.textfile)
        elif ".json" in self.textfile:
            import json

            self.storage.write([])
            self.record_list.delete(0, "end")
            with open(self._jsonfile, "r", encoding="utf-8") as f:
                self.storage.write(json.load(f))


class SaveAndCloseCommand(Command):
    def execute(self):
        self.app.destroy()


class SubmitNameCommand(Command):
    def execute(self):
        try:
            name = self.name_entry.get()
            if not name:
                raise EmptyNameError("Name cannot be empty!")
            self.link_entry.focus()
        except EmptyNameError as e:
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, e)
            self.app.focus()


class SubmitAllCommand(Command):
    def execute(self):
        try:
            name = self.name_entry.get()
            if not name:
                raise EmptyNameError("Name cannot be empty!")
            self.link_entry.focus()
            link = self.link_entry.get()
            if link:
                if not is_url_valid(link):
                    raise InvalidLinkError("Invalid link!")
            self.storage.save(name, link)
            self.name_entry.delete(0, "end")
            self.link_entry.delete(0, "end")
            self.record_list.insert("end", name)
            self.name_entry.focus()

        except InvalidLinkError as e:
            self.link_entry.delete(0, "end")
            self.link_entry.insert(0, e)
            self.app.focus()
        except EmptyNameError as e:
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, e)
            self.app.focus()
