import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable, TypedDict
from mod_manager.formatter import format_record
import time


class Record(TypedDict):
    text: str
    link: str


class RecordStorage(ABC):
    @abstractmethod
    def save(self, record) -> None: ...

    @abstractmethod
    def read(self) -> list: ...

    @abstractmethod
    def write(self, records) -> None: ...

    @abstractmethod
    def delete(self, indexes_to_delete: Iterable[int]) -> None: ...


class JSONFileRecordStorage(RecordStorage):
    def __init__(self, jsonfile: Path) -> None:
        self._jsonfile = jsonfile
        self._init_storage()

    def save(self, name: str, link: str) -> None:
        records = self.read()
        records.append({"name": name, "link": link})
        self.write(records)

    def _init_storage(self) -> None:
        if not self._jsonfile.exists():
            self._jsonfile.write_text("[]")

    def read(self) -> list[Record]:
        with open(self._jsonfile, "r", encoding="utf-8") as f:
            return json.load(f)

    def write(self, records: list[Record]) -> None:
        with open(self._jsonfile, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=4)

    def delete(self, indexes_to_delete: Iterable[int]) -> None:
        records = [
            record
            for index, record in enumerate(self.read())
            if index not in indexes_to_delete
        ]
        self.write(records)


class PlainTextRecordStorage(RecordStorage):
    def __init__(self, textfile: Path) -> None:
        self._textfile = textfile
        self._init_storage()
        

    def save(self):
        for index, text in enumerate(self.record_list.get(0, "end")):
            self.write(index)

    def write(self, index):
        with open(self._textfile, "w") as file:
            name, link = format_record(index, self.storage)
            file.write(f"Name: {name}\n")
            if link:
                file.write(f"Link: {link}\n")
            file.write("----\n")
    
    def delete():
        ...

    def _init_storage(self) -> None:
        if not self._textfile.exists():
            raise FileNotFoundError

    def read(self):
        records = []
        current_record = {}
        with open(self._textfile, "r") as f:
            for line in f:
                line = line.strip()  
                if not line:           
                    continue
                if line.startswith("----"):
                    records.append(current_record)
                if line.startswith("Name:"):
                    current_record["name"] = line.split(":")[1].strip()
                elif line.startswith("Link:"):
                    current_record["link"] = line.split(":")[1].strip()
            return records
