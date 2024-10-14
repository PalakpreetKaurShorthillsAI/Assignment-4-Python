from abc import ABC, abstractmethod

class FileLoader(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
    
    @abstractmethod
    def load_file(self):
        """Load the file and return its content."""
        pass

    @abstractmethod
    def validate_file(self):
        """Validate if the file is of correct type."""
        pass
