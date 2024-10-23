from pptx import Presentation

class PPTLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.presentation = None
        self.load_file()

    def load_file(self):
        """Load the PPT file and store its content."""
        try:
            self.presentation = Presentation(self.file_path)
        except Exception as e:
            print(f"Error loading PPT: {e}")
            self.presentation = None

    def get_content(self):
        """Return the content of the PPT file."""
        return self.presentation

    def close_file(self):
        """Close the PPT file if necessary."""
        pass  # Closing not necessary for python-pptx
