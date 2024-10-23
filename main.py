# import os
# from dotenv import load_dotenv
# from data_extractor.data_extractor import UniversalDataExtractor
# from file_loader.concrete_file_loader import Loader  # Import the common Loader class
# from storage.file_storage import FileStorage
# from storage.sql_storage import SQLStorage
# from tabulate import tabulate
 
# class Main:
#     def __init__(self):
#         load_dotenv()
#         self.db_config = {
#             'user': os.getenv('DB_USER'),
#             'password': os.getenv('DB_PASSWORD'),
#             'host': os.getenv('DB_HOST'),
#             'database': os.getenv('DB_NAME')
#         }
#         self.file_storage = FileStorage("output")
#         self.sql_storage = SQLStorage(self.db_config)
#         self.sql_storage.create_tables()
 
#     def get_user_file_path(self):
#         """Prompt the user for a file path and return it."""
#         file_path = input("Please enter the file path: ")
#         return file_path
 
 
#     def process_file(self, file_path, file_type):
#         """Load, extract, store, and print data using the common Loader."""
        
#         loader = Loader(file_path, file_type)  # Created an instance of the Loader class
#         loader.load_file()  # Load the file based on type (handled inside Loader class)
        
#         extractor = UniversalDataExtractor(loader)  # UniversalDataExtractor uses the loaded file
#         self.file_storage.store_data(extractor)
#         self.sql_storage.store_data(extractor)
 
#         # Print extracted data
#         # print("Extracted Data:\n",
#         #       "Text:", extractor.extract_text(), "\n",
#         #       "Tables:", tabulate(extractor.extract_tables(), headers='keys', tablefmt='grid'), "\n",
#         #       "Images:", extractor.extract_images(), "\n",
#         #       "Metadata:", extractor.extract_metadata(), "\n",
#         #       "Links:", extractor.extract_links(), "\n")
 
#     def run(self):
#         # Get file path from user input
#         file_path = self.get_user_file_path()
        
#         # Validate file type
#         file_type = os.path.splitext(file_path)[1][1:]
#         if file_type:
#             # Process the file using the common Loader and UniversalDataExtractor
#             self.process_file(file_path, file_type)
#         else:
#             print("File format not supported. Please provide a .pdf, .docx, or .pptx file.")
 
    
 
# if __name__ == "__main__":
#     main_instance = Main()
#     main_instance.run()


import os
from dotenv import load_dotenv
from data_extractor.data_extractor import UniversalDataExtractor
from file_loader.concrete_file_loader import Loader  # Import the common Loader class
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
 
    def get_user_file_path(self):
        """Prompt the user for a file path and return it."""
        file_path = input("Please enter the file path: ")
        return file_path
 
 
    def process_file(self, file_path, file_type):
        """Load, extract, store, and print data using the common Loader."""
        
        loader = Loader(file_path, file_type)  # Created an instance of the Loader class
        loader.load_file()  # Load the file based on type (handled inside Loader class)
        
        extractor = UniversalDataExtractor(loader)  # UniversalDataExtractor uses the loaded file
        self.file_storage.store_data(extractor)
        self.sql_storage.store_data(extractor)
 
        
    def run(self):
        # Get file path from user input
        file_path = self.get_user_file_path()
 
        # Validate file type
        file_type = os.path.splitext(file_path)[1][1:]
        if file_type:
            # Process the file using the common Loader and UniversalDataExtractor
            self.process_file(file_path, file_type)
        else:
            print("File format not supported. Please provide a .pdf, .docx, or .pptx file.")
 
    
 
if __name__ == "__main__":
    main_instance = Main()
    main_instance.run()