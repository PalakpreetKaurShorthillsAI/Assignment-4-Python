from file_loader.pdf_loader import PDFLoader
from file_loader.docx_loader import DOCXLoader
from file_loader.ppt_loader import PPTLoader
from storage.file_storage import FileStorage  # Correct import for FileStorage
from storage.sql_storage import SQLStorage
from data_extractor.data_extractor import DataExtractor

from storage.sql_storage import SQLStorage


def test_pdf():
    pdf_loader = PDFLoader('samples/Sample_file.pdf')  # Make sure the file path is correct
    extractor = DataExtractor(pdf_loader)
    text_data = extractor.extract_text()
    print("PDF Text Data:", text_data)

def test_docx():
    docx_loader = DOCXLoader('samples/Sample_file.docx')  # Make sure the file path is correct
    extractor = DataExtractor(docx_loader)
    text_data = extractor.extract_text()
    print("DOCX Text Data:", text_data)

def test_ppt():
    ppt_loader = PPTLoader('samples/Sample_file.pptx')  # Make sure the file path is correct
    extractor = DataExtractor(ppt_loader)
    text_data = extractor.extract_text()
    print("PPT Text Data:", text_data)

def test_file_storage():
    """Test storing data using FileStorage."""
    pdf_loader = PDFLoader("samples/Sample_file.pdf")  # Load your PDF file
    extractor = DataExtractor(pdf_loader)
    
    # Initialize FileStorage and store data
    file_storage = FileStorage(output_dir="output")
    file_storage.store_data(extractor)
    print("Data stored in files.")

def test_sql_storage():
    """Test storing data using SQLStorage."""
    pdf_loader = PDFLoader("samples/Sample_file.pdf")  # Load your PDF file
    extractor = DataExtractor(file_loader=pdf_loader)
    
    # Initialize SQLStorage and store data in SQLite database
    sql_storage = SQLStorage(extractor=extractor)
    sql_storage.store_data()
   
    print("Data stored in SQL database.")


if __name__ == '__main__':
    test_pdf()  # Test PDF extraction
    test_docx()  # Test DOCX extraction
    test_ppt()  # Test PPT extraction
    test_file_storage()
    test_sql_storage()