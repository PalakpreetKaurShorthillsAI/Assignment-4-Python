import os
from dotenv import load_dotenv
from data_extractor import PDFDataExtractor, DOCXDataExtractor, PPTDataExtractor
from file_loader.pdf_loader import PDFLoader
from file_loader.docx_loader import DOCXLoader
from file_loader.ppt_loader import PPTLoader
from storage.file_storage import FileStorage
from storage.sql_storage import SQLStorage
from tabulate import tabulate
 
class Main:
    def __init__(self):
        load_dotenv()
        self.db_config = {
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME')
        }
        self.file_storage = FileStorage("output")
        self.sql_storage = SQLStorage(self.db_config)
        self.sql_storage.create_tables()
 
    def process_file(self, file_path, loader_class, extractor_class):
        """Load, extract, store, and print data."""
        loader = loader_class(file_path)
        loader.load_file()
        extractor = extractor_class(loader)
        
        self.file_storage.store_data(extractor)
        self.sql_storage.store_data(extractor)
        
        print("Extracted Data:\n",
              "Text:", extractor.extract_text(), "\n",
              "Tables:", tabulate(extractor.extract_tables(), headers='keys', tablefmt='grid'), "\n",
              "Images:", extractor.extract_images(), "\n",
              "Metadata:", extractor.extract_metadata(), "\n",
              "Links:", extractor.extract_links(), "\n")
 
    def run(self):
        """Run the pipeline for all file types."""
        file_paths = {
            'pdf': ('test_files/PDF/sample.pdf', PDFLoader, PDFDataExtractor),
            'docx': ('test_files/DOCX/sample.docx', DOCXLoader, DOCXDataExtractor),
            'pptx': ('test_files/PPT/sample.pptx', PPTLoader, PPTDataExtractor)
        }
 
        for file_type, (path, loader, extractor) in file_paths.items():
            self.process_file(path, loader, extractor)
 
    def close(self):
        """Close the SQL database connection."""
        self.sql_storage.close_connection()
 
if __name__ == "__main__":
    main_instance = Main()
    main_instance.run()
    main_instance.close()