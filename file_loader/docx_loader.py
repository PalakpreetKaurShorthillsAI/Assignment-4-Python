import docx

class DOCXLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_file(self):
        """Load and return a Document object."""
        return docx.Document(self.file_path)

    def validate_file(self):
        """Check if the file exists at the given path."""
        pass  # Add file validation logic if needed
