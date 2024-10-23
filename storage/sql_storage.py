import mysql.connector  # For connecting to MySQL
from mysql.connector import Error  # For handling MySQL errors

class SQLStorage:
    def __init__(self, db_config):
        """
        Initialize the SQLStorage class with database configuration and create connection.
        
        Args:
            db_config (dict): A dictionary containing the database credentials.
        """
        self.db_config = db_config  # Store the database configuration
        self.connection = None  # Connection object to be established
        self.create_connection()  # Establish the connection when the class is instantiated

    def create_connection(self):
        """Create a database connection using the provided db_config."""
        try:
            # Create a connection to the MySQL database
            connection = mysql.connector.connect(
                user=self.db_config['user'],
                password=self.db_config['password'],
                host=self.db_config['host'],
                database=self.db_config['database']
            )
            if connection.is_connected():
                self.connection = connection  # Set the connection if successful
                print("Connection to MySQL established")
        except mysql.connector.Error as e:
            # Handle connection errors
            print(f"Error connecting to MySQL: {e}")
            self.connection = None

    def create_tables(self):
        """Create tables for storing extracted data in the database."""
        if self.connection is None:
            print("No database connection. Cannot create tables.")
            return

        # SQL statements to create necessary tables
        create_statements = [
            """
            CREATE TABLE IF NOT EXISTS extracted_files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_name VARCHAR(255) NOT NULL,
                file_type VARCHAR(50),
                extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS extracted_texts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_id INT,
                text LONGTEXT,
                FOREIGN KEY (file_id) REFERENCES extracted_files(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS extracted_tables (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_id INT,
                table_data LONGTEXT,
                FOREIGN KEY (file_id) REFERENCES extracted_files(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS extracted_images (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_id INT,
                image_path VARCHAR(255),
                FOREIGN KEY (file_id) REFERENCES extracted_files(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS extracted_metadata (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_id INT,
                metadata_key VARCHAR(255),
                metadata_value TEXT,
                FOREIGN KEY (file_id) REFERENCES extracted_files(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS extracted_links (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_id INT,
                link VARCHAR(255),
                FOREIGN KEY (file_id) REFERENCES extracted_files(id)
            )
            """
        ]

        cursor = self.connection.cursor()  # Cursor to execute SQL commands
        try:
            # Execute each SQL statement to create tables
            for statement in create_statements:
                cursor.execute(statement)
            self.connection.commit()  # Commit changes to the database
            print("Tables created successfully.")
        except Error as e:
            # Handle errors during table creation
            print(f"Error creating tables: {e}")
        finally:
            cursor.close()  # Close the cursor after operation

    def store_data(self, extractor):
        """Store extracted data from the extractor into the database."""
        if self.connection is None:
            print("No database connection. Cannot store data.")
            return

        file_name = extractor.get_file_name()  # Get the file name from the extractor
        file_type = extractor.__class__.__name__  # Get the file type (extractor class name)

        cursor = self.connection.cursor()  # Cursor for executing SQL commands
        try:
            # Insert file metadata and get the generated file ID
            file_id = self.insert_file(cursor, file_name, file_type)

            # Insert the extracted data into the respective tables
            self.insert_text(cursor, extractor, file_id)
            self.insert_tables(cursor, extractor, file_id)
            self.insert_images(cursor, extractor, file_id)
            self.insert_metadata(cursor, extractor, file_id)
            self.insert_links(cursor, extractor, file_id)

            self.connection.commit()  # Commit the transaction
            print("Data stored successfully.")

        except Error as e:
            # Handle any errors during data insertion
            print(f"Error storing data: {e}")
            self.connection.rollback()  # Rollback changes in case of an error
        finally:
            cursor.close()  # Close the cursor

    def insert_file(self, cursor, file_name, file_type):
        """
        Insert the file record into the database and return the generated file_id.

        Args:
            cursor: Database cursor to execute SQL commands.
            file_name (str): The name of the file.
            file_type (str): The type of the file.

        Returns:
            int: The ID of the inserted file.
        """
        cursor.execute(
            "INSERT INTO extracted_files (file_name, file_type) VALUES (%s, %s)",
            (file_name, file_type)
        )
        return cursor.lastrowid  # Return the ID of the inserted file

    def insert_text(self, cursor, extractor, file_id):
        """
        Insert extracted text into the database.

        Args:
            cursor: Database cursor to execute SQL commands.
            extractor: The extractor object containing extracted data.
            file_id (int): The ID of the file.
        """
        text = extractor.extract_text()  # Get extracted text from the extractor
        if text:
            cursor.execute(
                "INSERT INTO extracted_texts (file_id, text) VALUES (%s, %s)",
                (file_id, text)
            )

    def insert_tables(self, cursor, extractor, file_id):
        """
        Insert extracted tables into the database.

        Args:
            cursor: Database cursor to execute SQL commands.
            extractor: The extractor object containing extracted data.
            file_id (int): The ID of the file.
        """
        tables = extractor.extract_tables()  # Get extracted tables from the extractor
        for table in tables:
            # Convert the table data to a comma-separated string
            table_data = '\n'.join([','.join(row) for row in table])
            cursor.execute(
                "INSERT INTO extracted_tables (file_id, table_data) VALUES (%s, %s)",
                (file_id, table_data)
            )

    def insert_images(self, cursor, extractor, file_id):
        """
        Insert extracted images into the database.

        Args:
            cursor: Database cursor to execute SQL commands.
            extractor: The extractor object containing extracted data.
            file_id (int): The ID of the file.
        """
        images = extractor.extract_images()  # Get extracted images from the extractor
        for image_path in images:
            cursor.execute(
                "INSERT INTO extracted_images (file_id, image_path) VALUES (%s, %s)",
                (file_id, image_path)
            )

    def insert_metadata(self, cursor, extractor, file_id):
        """
        Insert extracted metadata into the database.

        Args:
            cursor: Database cursor to execute SQL commands.
            extractor: The extractor object containing extracted data.
            file_id (int): The ID of the file.
        """
        metadata = extractor.extract_metadata()  # Get extracted metadata from the extractor
        if isinstance(metadata, dict):
            for key, value in metadata.items():
                if value:  # Only insert non-empty metadata
                    cursor.execute(
                        "INSERT INTO extracted_metadata (file_id, metadata_key, metadata_value) VALUES (%s, %s, %s)",
                        (file_id, key, value)
                    )

    def insert_links(self, cursor, extractor, file_id):
        """
        Insert extracted links into the database.

        Args:
            cursor: Database cursor to execute SQL commands.
            extractor: The extractor object containing extracted data.
            file_id (int): The ID of the file.
        """
        links = extractor.extract_links()  # Get extracted links from the extractor
        for link in links:
            cursor.execute(
                "INSERT INTO extracted_links (file_id, link) VALUES (%s, %s)",
                (file_id, link)
            )

    def close_connection(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()  # Close the connection if it is open
            print("Database connection closed.")
