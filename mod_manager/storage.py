import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable, TypedDict
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


# class PlainTextRecordStorage(RecordStorage):
#     def __init__(self, textfile: Path) -> None:
#         self._textfile = textfile
#         self._init_storage()

#     def save(self, name:)
