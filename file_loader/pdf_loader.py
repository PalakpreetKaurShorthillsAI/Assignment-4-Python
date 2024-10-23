import pdfplumber

class PDFLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.pdf = None
        self.content = None
        self.load_pdf()  # Load the PDF immediately during initialization

    def load_pdf(self):
        """Load the PDF file and store its content."""
        try:
            self.pdf = pdfplumber.open(self.file_path)
            self.content = self.pdf.pages  # Store all pages
        except Exception as e:
            print(f"Error loading PDF: {e}")
            self.content = None

    def load_file(self):
        """Return the loaded content (in this case, the pages of the PDF)."""
        return self.content

    def close_pdf(self):
        """Close the PDF file."""
        if self.pdf:
            self.pdf.close()



