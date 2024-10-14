from PyPDF2 import PdfReader

class PDFLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_file(self):
        """Load and return a PdfReader object."""
        return PdfReader(self.file_path)

    def validate_file(self):
        """Check if the file exists at the given path."""
        pass  # Add file validation logic if needed
