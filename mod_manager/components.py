import tkinter as tk
from typing import Callable

from mod_manager import config


class RecordListFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, background=config.DARK_GREY)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.listbox = self._create_listbox()

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.grid(row=0, column=0)
        self.listbox.pack(pady=7, padx=7)

    def _create_listbox(self) -> tk.Listbox:
        listbox = tk.Listbox(
            self,
            width=40,
            height=30,
            font=("monaco 20"),
            yscrollcommand=self.scrollbar.set,
            background=config.DARK_GREY,
            highlightthickness=2,
            fg="WHITE",
            selectmode=tk.EXTENDED,
            highlightbackground=config.DARK_GREY,
            highlightcolor=config.DARK_GREY,
        )
        self.scrollbar.config(command=listbox.yview)
        return listbox


class ButtonsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, background=config.GREY)

        self.delete_button = self._create_button("Delete", None, fg=config.RED)
        self.delete_all_button = self._create_button("Delete All", None, fg=config.RED)
        self.edit_button = self._create_button("Edit", None)
        self.copy_button = self._create_button("Copy", None)
        self.export_to_file_button = self._create_button("Export", None)
        self.import_from_file_button = self._create_button("Import", None)
        self.save_and_close_button = self._create_button("Save and Close", None)

        self.grid(row=0, column=1, pady=7, sticky="sn")

    def _create_button(
        self, text: str, command: Callable, fg: str = "WHITE"
    ) -> tk.Button:
        button = tk.Button(
            self,
            text=text,
            command=command,
            font="monaco",
            fg=fg,
            bg=config.GREY,
        )
        button.pack(side=tk.TOP, fill=tk.BOTH, pady=7, padx=7)
        return button


class NameEntry(tk.Entry):
    def __init__(self, parent):
        super().__init__(
            parent, font=("monaco", 13), background=config.GREY, fg="WHITE"
        )
        self.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=7,
            pady=7,
            sticky="ew",
        )

class LinkEntry(tk.Entry):
    def __init__(self, parent):
        super().__init__(
            parent, font=("monaco", 13), background=config.GREY, fg="WHITE"
        )
        self.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=7,
            pady=7,
            sticky="ew",
        )
