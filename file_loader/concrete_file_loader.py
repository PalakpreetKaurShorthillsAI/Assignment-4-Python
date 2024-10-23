import pdfplumber  # Library for handling PDF files
from docx import Document  # Library for handling Word documents
from pptx import Presentation  # Library for handling PowerPoint presentations
from abc import ABC, abstractmethod  # For creating an abstract base class
import os  # For file handling operations

# Abstract class FileLoader
class FileLoader(ABC):
    def __init__(self, file_path, file_type):
        """
        Initialize the FileLoader with file path and file type.
        
        Args:
            file_path (str): The path to the file to be loaded.
            file_type (str): The file type (extension) to determine the loader.
        """
        self.file_path = file_path  # Store the file path
        self.file_type = file_type  # Extracts the file extension (e.g., 'pdf', 'docx', 'pptx')
        self.file = None  # Will store the file object after loading
 
    @abstractmethod
    def load_file(self):
        """
        Abstract method to load the file based on its type.
        Must be implemented by concrete subclasses.
        """
        pass
 
    def validate_file(self):
        """
        Validate the file by checking if it exists and is of a supported type.
        
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file type is unsupported.
        """
        if not os.path.exists(self.file_path):
            # Check if the file exists at the specified path
            raise FileNotFoundError(f"File does not exist: {self.file_path}")
        if self.file_type not in ['pdf', 'docx', 'pptx']:
            # Ensure the file type is one of the supported types
            raise ValueError(f"Unsupported file type: {self.file_type}. Only PDF, DOCX, and PPTX are supported.")

# Concrete Loader class that handles loading of files
class Loader(FileLoader):
    # A dictionary mapping file types to their respective file readers
    file_reader = {
        'pdf': pdfplumber.open,  # pdfplumber for PDF files
        'docx': Document,  # Document for Word files
        'pptx': Presentation,  # Presentation for PowerPoint files
    }
 
    def load_file(self):
        """
        Load the file based on the file type after validation.
        
        Raises:
            ValueError: If there's an error loading the file.
        """
        self.validate_file()  # First validate the file (check existence and type)
 
        try:
            # Load the file using the appropriate method from the file_reader dictionary
            self.file = self.file_reader[self.file_type](self.file_path)
        except Exception as e:
            # Raise an error if there's an issue loading the file
            raise ValueError(f"Error loading file: {e}")
