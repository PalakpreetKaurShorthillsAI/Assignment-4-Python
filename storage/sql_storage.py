# storage/sql_storage.py
import mysql.connector
from storage.storage import Storage

class SQLStorage(Storage):
    def __init__(self, extractor):
        self.extractor = extractor
        # MySQL connection details
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Palak030102',
            database='extracted_data_db'
        )
        self.cursor = self.conn.cursor()

    def store_data(self):
        # Initialize text_data at the beginning
        text_data = self.extractor.extract_text()

        # Debugging output for extracted text data
        print(f"Extracted text data: {text_data}")

        # Check if text_data is None or empty
        if text_data is None:
            print("No text data extracted.")
            return

        # Handle text_data based on its type
        if isinstance(text_data, dict):
            print(f"Keys in text_data: {text_data.keys()}")  # Show keys in dictionary
            text_content = text_data.get('text', '')  # Adjust the key to match actual data
        else:
            text_content = str(text_data)  # Ensure it's a string

        # Debugging output for final text content
        print(f"Final text content to be stored: {text_content}")

        # Insert into the database
        self.cursor.execute("INSERT INTO extracted_texts (content) VALUES (%s)", (text_content,))
        self.conn.commit()

        
        
        
        tables = self.extractor.extract_tables()
        images = self.extractor.extract_images()


        print(f"Text to be stored: {text_content}")  # Ensure it's a string
        # Create tables if they don't exist and insert the extracted text
        # self.cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS TextData (
        #         id INT AUTO_INCREMENT PRIMARY KEY,
        #         content TEXT
        #     )
        # """)
        

        # Similarly, create tables for tables and images and insert the data
        # Store tables
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS TableData (
                id INT AUTO_INCREMENT PRIMARY KEY,
                table_content TEXT
            )
        """)
        for table in tables:
            self.cursor.execute("INSERT INTO TableData (table_content) VALUES (%s)", (str(table),))
        self.conn.commit()

        # Store images (assuming they are in binary format)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ImageData (
                id INT AUTO_INCREMENT PRIMARY KEY,
                image_data BLOB
            )
        """)
        for img_data in images:
            self.cursor.execute("INSERT INTO ImageData (image_data) VALUES (%s)", (img_data,))
        self.conn.commit()
    

    def close(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()

    def __del__(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
