import json
from abc import ABC, abstractmethod


class BaseLoader(ABC):
    def __init__(self, connection, file_path: str):
        self.connection = connection
        self.file_path = file_path

    def load_json(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    @abstractmethod
    def insert(self, data: list):
        pass

    def run(self):
        data = self.load_json()
        self.insert(data)
