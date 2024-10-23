import pdfplumber
from docx import Document
from pptx import Presentation
from abc import ABC, abstractmethod
import os
 
# Abstract class FileLoader
class FileLoader(ABC):
    def __init__(self, file_path, file_type):
        self.file_path = file_path
        self.file_type = file_type # Extracts the file extension
        self.file = None
 
    @abstractmethod
    def load_file(self):
        """Abstract method to load the file based on the file type."""
        pass
 
    def validate_file(self):
        """Validate that the file exists and its type is supported."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File does not exist: {self.file_path}")
        if self.file_type not in ['pdf', 'docx', 'pptx']:
            raise ValueError(f"Unsupported file type: {self.file_type}. Only PDF, DOCX, and PPTX are supported.")
 
# Concrete Loader class that handles loading of files
class Loader(FileLoader):
 
    file_reader = {
        'pdf': pdfplumber.open,
        'docx': Document,
        'pptx': Presentation,
    }
 
    def load_file(self):
        """Load the file based on the file type."""
        self.validate_file()  # First validate the file
 
        try:
            self.file = self.file_reader[self.file_type](self.file_path)
        except Exception as e:
            raise ValueError(f"Error loading file: {e}")
