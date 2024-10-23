import os
from dotenv import load_dotenv  # Load environment variables from a .env file
from data_extractor.data_extractor import UniversalDataExtractor  # Universal extractor for different file types
from file_loader.concrete_file_loader import Loader  # Import the Loader class for loading files
from storage.file_storage import FileStorage  # Handles file-based storage of extracted data
from storage.sql_storage import SQLStorage  # Handles database storage of extracted data
from tabulate import tabulate  # Optional: for tabular display of data (not used in the current code)
 
class Main:
    def __init__(self):
        load_dotenv()  # Load database credentials from .env file

        # Database configuration loaded from environment variables
        self.db_config = {
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME')
        }

        # File storage for storing extracted data into local files
        self.file_storage = FileStorage("output")

        # SQL storage for storing extracted data into a MySQL database
        self.sql_storage = SQLStorage(self.db_config)

        # Create necessary tables in the database if they don't already exist
        self.sql_storage.create_tables()
 
    def get_user_file_path(self):
        """
        Prompt the user for a file path and return it.
        This method handles user input for file selection.
        """
        file_path = input("Please enter the file path: ")
        return file_path
 
 
    def process_file(self, file_path, file_type):
        """
        Load the file, extract data, and store it using both file and database storage.

        Args:
            file_path (str): The path to the file to be processed.
            file_type (str): The type/extension of the file (e.g., 'pdf', 'docx', 'pptx').
        """
        # Create an instance of Loader for loading the file
        loader = Loader(file_path, file_type)
        
        # Load the file based on its type (the logic is handled inside the Loader class)
        loader.load_file()
        
        # Use UniversalDataExtractor to extract data from the loaded file
        extractor = UniversalDataExtractor(loader)

        # Store the extracted data in file-based storage
        self.file_storage.store_data(extractor)

        # Store the extracted data in SQL storage (MySQL database)
        self.sql_storage.store_data(extractor)
 
        
    def run(self):
        """
        Main logic to execute the program.
        This includes getting the file path from the user, validating the file type, and processing the file.
        """
        # Get file path from user input
        file_path = self.get_user_file_path()
 
        # Extract the file extension (e.g., 'pdf', 'docx', 'pptx')
        file_type = os.path.splitext(file_path)[1][1:]

        # Validate file type before processing
        if file_type:
            # Process the file using the Loader and UniversalDataExtractor
            self.process_file(file_path, file_type)
        else:
            print("File format not supported. Please provide a .pdf, .docx, or .pptx file.")
 
    
 
if __name__ == "__main__":
    # Create an instance of the Main class and run the application
    main_instance = Main()
    main_instance.run()
