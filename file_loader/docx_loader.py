from docx import Document

class DOCXLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.document = None
        self.load_file()

    def load_file(self):
        """Load the DOCX file and store its content."""
        try:
            self.document = Document(self.file_path)
        except Exception as e:
            print(f"Error loading DOCX: {e}")
            self.document = None

    def get_content(self):
        """Return the content of the DOCX file."""
        return self.document

    def close_file(self):
        """Close the DOCX file if necessary."""
        pass  # Closing not necessary for python-docx


