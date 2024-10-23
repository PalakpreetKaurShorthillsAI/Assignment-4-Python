import mysql.connector
from mysql.connector import Error


class SQLStorage:
    def __init__(self, db_config):
        """Initialize the SQLStorage class with database configuration and create connection."""
        self.db_config = db_config
        self.connection = None
        self.create_connection()  # Ensure connection is established when the class is instantiated

    def create_connection(self):
        """Create a database connection."""
        try:
            connection = mysql.connector.connect(
                user=self.db_config['user'],
                password=self.db_config['password'],
                host=self.db_config['host'],
                database=self.db_config['database']
            )
            if connection.is_connected():
                self.connection = connection
                print("Connection to MySQL established")
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None

    def create_tables(self):
        """Create tables for storing extracted data."""
        if self.connection is None:
            print("No database connection. Cannot create tables.")
            return

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

        cursor = self.connection.cursor()
        try:
            for statement in create_statements:
                cursor.execute(statement)
            self.connection.commit()
            print("Tables created successfully.")
        except Error as e:
            print(f"Error creating tables: {e}")
        finally:
            cursor.close()

    def store_data(self, extractor):
        """Store extracted data into the database."""
        if self.connection is None:
            print("No database connection. Cannot store data.")
            return

        file_name = extractor.get_file_name()
        file_type = extractor.__class__.__name__

        cursor = self.connection.cursor()
        try:
            file_id = self.insert_file(cursor, file_name, file_type)

            self.insert_text(cursor, extractor, file_id)
            self.insert_tables(cursor, extractor, file_id)
            self.insert_images(cursor, extractor, file_id)
            self.insert_metadata(cursor, extractor, file_id)
            self.insert_links(cursor, extractor, file_id)

            self.connection.commit()
            print("Data stored successfully.")

        except Error as e:
            print(f"Error storing data: {e}")
            self.connection.rollback()  # Rollback in case of error
        finally:
            cursor.close()

    def insert_file(self, cursor, file_name, file_type):
        """Insert the file record into the database and return the generated file_id."""
        cursor.execute(
            "INSERT INTO extracted_files (file_name, file_type) VALUES (%s, %s)",
            (file_name, file_type)
        )
        return cursor.lastrowid  # Get the id of the inserted file

    def insert_text(self, cursor, extractor, file_id):
        """Insert extracted text into the database."""
        text = extractor.extract_text()
        if text:
            cursor.execute(
                "INSERT INTO extracted_texts (file_id, text) VALUES (%s, %s)",
                (file_id, text)
            )

    def insert_tables(self, cursor, extractor, file_id):
        """Insert extracted tables into the database."""
        tables = extractor.extract_tables()
        for table in tables:
            table_data = '\n'.join([','.join(row) for row in table])
            cursor.execute(
                "INSERT INTO extracted_tables (file_id, table_data) VALUES (%s, %s)",
                (file_id, table_data)
            )

    def insert_images(self, cursor, extractor, file_id):
        """Insert extracted images into the database."""
        images = extractor.extract_images()
        for image_path in images:
            cursor.execute(
                "INSERT INTO extracted_images (file_id, image_path) VALUES (%s, %s)",
                (file_id, image_path)
            )

    def insert_metadata(self, cursor, extractor, file_id):
        """Insert extracted metadata into the database."""
        metadata = extractor.extract_metadata()
        if isinstance(metadata, dict):
            for key, value in metadata.items():
                if value:
                    cursor.execute(
                        "INSERT INTO extracted_metadata (file_id, metadata_key, metadata_value) VALUES (%s, %s, %s)",
                        (file_id, key, value)
                    )

    def insert_links(self, cursor, extractor, file_id):
        """Insert extracted links into the database."""
        links = extractor.extract_links()
        for link in links:
            cursor.execute(
                "INSERT INTO extracted_links (file_id, link) VALUES (%s, %s)",
                (file_id, link)
            )

    def close_connection(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")
