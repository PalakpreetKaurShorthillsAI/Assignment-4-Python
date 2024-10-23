import os
import csv
from data_extractor.data_extractor import UniversalDataExtractor  # Import the universal data extractor
from file_loader.concrete_file_loader import Loader  # Import the common Loader class to load different file types
from PIL import Image  # Import Pillow library for handling images
import io  # Used for handling byte streams of images
from tabulate import tabulate  # Importing tabulate for pretty table display in the terminal
 
class FileStorage:
    def __init__(self, output_dir):
        """
        Initialize the FileStorage with an output directory.
        Args:
            output_dir (str): The directory where extracted data will be saved.
        """
        self.output_dir = output_dir
 
    def store_data(self, extractor):
        """
        Store data extracted by the UniversalDataExtractor.
        This includes saving text, tables, images, metadata, and links to files.

        Args:
            extractor (UniversalDataExtractor): The data extractor that provides the extracted data.
        """
        # Create a base folder for storing all extracted content for the file
        base_folder = os.path.join(self.output_dir, extractor.get_file_name())
        os.makedirs(base_folder, exist_ok=True)  # Ensure the directory exists
 
        # Store extracted text data
        data = extractor.extract_text()
        if data and 'text' in data and data['text'].strip():
            # Save text to a file if extracted
            text_file_path = os.path.join(base_folder, "extracted_text.txt")
            with open(text_file_path, 'w', encoding='utf-8') as text_file:
                text_file.write(data['text'])
            print(f"Text data saved to {text_file_path}")
        else:
            print("Text data extracted.")
 
        # Store extracted tables
        tables = extractor.extract_tables()
        if tables:
            # Create a folder for storing tables
            tables_folder = os.path.join(base_folder, "tables")
            os.makedirs(tables_folder, exist_ok=True)
            for i, table in enumerate(tables):
                # Save each table as a CSV file
                csv_file_path = os.path.join(tables_folder, f"table_{i + 1}.csv")
                with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(table)
                print(f"Table data saved to {csv_file_path}")
                # Display the table in a pretty format in the terminal
                print(f"Table {i + 1}:\n{tabulate(table, headers='keys', tablefmt='grid')}")
        else:
            print("No tables extracted.")
 
        # Store extracted images
        images = extractor.extract_images()
        if images:
            # Create a folder for storing images
            images_folder = os.path.join(base_folder, "images")
            os.makedirs(images_folder, exist_ok=True)
            for i, img_info in enumerate(images):
                # Check if the image is valid and has a stream of data
                if isinstance(img_info, dict) and 'stream' in img_info:
                    img_stream = img_info['stream']
                    img_data = img_stream.get_rawdata()  # Get the raw image data
 
                    # Convert image data to a Pillow image object
                    try:
                        img = Image.open(io.BytesIO(img_data))  # Open image from byte stream
                        img_path = os.path.join(images_folder, f"image_{i + 1}.png")
                        img.save(img_path)  # Save the image as a PNG file
                        print(f"Image saved to {img_path}")
                    except Exception as e:
                        print(f"Error saving image {i + 1}: {e}")
                else:
                    print(f"Image data for image {i + 1} is not valid or not found.")
        else:
            print("No images extracted.")
 
        # Store extracted metadata
        metadata = extractor.extract_metadata()
        if metadata:
            # Save metadata to a text file
            metadata_file_path = os.path.join(base_folder, "metadata.txt")
            with open(metadata_file_path, 'w', encoding='utf-8') as metadata_file:
                if isinstance(metadata, dict):
                    # Write metadata key-value pairs if metadata is a dictionary
                    for key, value in metadata.items():
                        if value:  # Only save non-empty metadata
                            metadata_file.write(f"{key}: {value}\n")
                else:
                    # Write metadata attributes if metadata is an object
                    for prop in dir(metadata):
                        if not prop.startswith('_') and prop != 'xml':  # Skip private/protected attributes
                            value = getattr(metadata, prop)
                            if value:  # Only save non-empty metadata
                                metadata_file.write(f"{prop}: {value}\n")
            print(f"Metadata saved to {metadata_file_path}")
        else:
            print("No metadata extracted.")
 
        # Store extracted links
        links = extractor.extract_links()
        unique_links = set(filter(None, links))  # Filter out empty links and remove duplicates
        if unique_links:
            # Save links to a text file
            links_file_path = os.path.join(base_folder, "extracted_links.txt")
            with open(links_file_path, 'w', encoding='utf-8') as links_file:
                for link in unique_links:
                    links_file.write(f"{link}\n")
            print(f"Links data saved to {links_file_path}")
        else:
            print("No links extracted.")
