# from PyPDF2 import PdfReader

# class PDFLoader:
#     def __init__(self, file_path):
#         self.file_path = file_path

#     def load_file(self):
#         """Load and return a PdfReader object."""
#         return PdfReader(self.file_path)

#     def validate_file(self):
#         """Check if the file exists at the given path."""
#         pass  # Add file validation logic if needed


# import os

# class PDFLoader:
#     def __init__(self, file_path):
#         self.file_path = file_path

#     def load_file(self):
#         # Load the PDF file (implement logic to load the file)
#         pass

#     def get_file_name(self):
#         """Extract the file name from the file path."""
#         return os.path.splitext(os.path.basename(self.file_path))[0]


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



