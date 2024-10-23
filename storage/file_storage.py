import os
import csv
from data_extractor.data_extractor import UniversalDataExtractor
from file_loader.concrete_file_loader import Loader  # Import the common Loader class
from PIL import Image
import io
from tabulate import tabulate  # Importing tabulate for pretty table display
 
class FileStorage:
    def __init__(self, output_dir):
        """Initialize the FileStorage with an output directory."""
        self.output_dir = output_dir
 
    def store_data(self, extractor):
        """Store data extracted by the extractor."""
        # Create a directory for storing extracted files
        base_folder = os.path.join(self.output_dir, extractor.get_file_name())
        os.makedirs(base_folder, exist_ok=True)
 
        # Store extracted text
        data = extractor.extract_text()
        if data and 'text' in data and data['text'].strip():
            text_file_path = os.path.join(base_folder, "extracted_text.txt")
            with open(text_file_path, 'w', encoding='utf-8') as text_file:
                text_file.write(data['text'])
            print(f"Text data saved to {text_file_path}")
        else:
            print("Text data extracted.")
 
        # Store tables
        tables = extractor.extract_tables()
        if tables:
            tables_folder = os.path.join(base_folder, "tables")
            os.makedirs(tables_folder, exist_ok=True)
            for i, table in enumerate(tables):
                csv_file_path = os.path.join(tables_folder, f"table_{i + 1}.csv")
                with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(table)
                print(f"Table data saved to {csv_file_path}")
                print(f"Table {i + 1}:\n{tabulate(table, headers='keys', tablefmt='grid')}")  # Displaying table in terminal
        else:
            print("Tables extracted.")
 
        # Store images
        images = extractor.extract_images()
        if images:
            images_folder = os.path.join(base_folder, "images")
            os.makedirs(images_folder, exist_ok=True)
            for i, img_info in enumerate(images):
                if isinstance(img_info, dict) and 'stream' in img_info:
                    img_stream = img_info['stream']
                    img_data = img_stream.get_rawdata()
 
                    # Convert PDFStream to a Pillow image
                    try:
                        img = Image.open(io.BytesIO(img_data))
                        img_path = os.path.join(images_folder, f"image_{i + 1}.png")
                        img.save(img_path)
                        print(f"Image saved to {img_path}")
                    except Exception as e:
                        print(f"Error saving image {i + 1}: {e}")
                else:
                    print(f"Image data for image {i + 1} is not valid or not found.")
        else:
            print("No images extracted.")
 
        # Store general metadata
        metadata = extractor.extract_metadata()
        if metadata:
            metadata_file_path = os.path.join(base_folder, "metadata.txt")
            with open(metadata_file_path, 'w', encoding='utf-8') as metadata_file:
                if isinstance(metadata, dict):
                    for key, value in metadata.items():
                        if value:  # Only save non-empty values
                            metadata_file.write(f"{key}: {value}\n")
                else:
                    for prop in dir(metadata):
                        if not prop.startswith('_') and prop != 'xml':
                            value = getattr(metadata, prop)
                            if value:  # Only save non-empty values
                                metadata_file.write(f"{prop}: {value}\n")
            print(f"Metadata saved to {metadata_file_path}")
        else:
            print("No metadata extracted.")
 
        # Store extracted links
        links = extractor.extract_links()
        unique_links = set(filter(None, links))
        if unique_links:
            links_file_path = os.path.join(base_folder, "extracted_links.txt")
            with open(links_file_path, 'w', encoding='utf-8') as links_file:
                for link in unique_links:
                    links_file.write(f"{link}\n")
            print(f"Links data saved to {links_file_path}")
        else:
            print("No links extracted.")