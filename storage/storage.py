# storage/storage.py
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def store_data(self):
        pass
