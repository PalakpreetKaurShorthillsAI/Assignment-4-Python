# storage/file_storage.py

import os
import csv
import shutil

class FileStorage:
    def __init__(self, output_dir):
        """Initialize with a directory to store the files."""
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def store_data(self, extractor):
        """Store data from the DataExtractor instance to files."""
        data = extractor.extract_text()

        # Store text
        text_file_path = os.path.join(self.output_dir, "extracted_text.txt")
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(data['text'])
        print(f"Text data saved to {text_file_path}")

        # Store tables
        tables = extractor.extract_tables()
        if tables:
            for i, table in enumerate(tables):
                csv_file_path = os.path.join(self.output_dir, f"table_{i+1}.csv")
                with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(table)
                print(f"Table data saved to {csv_file_path}")

        # Store images
        # images = extractor.extract_images()
        # if images:
        #     image_dir = os.path.join(self.output_dir, "images")
        #     if not os.path.exists(image_dir):
        #         os.makedirs(image_dir)
        #     for i, img_data in enumerate(images):
        #         img_file_path = os.path.join(image_dir, f"image_{i+1}.jpg")
        #         with open(img_file_path, 'wb') as img_file:
        #             img_file.write(img_data)
        #         print(f"Image saved to {img_file_path}")

        images = extractor.extract_images()
        for img_path in images:
            # img_path already points to a saved image file, so no need to write img_data
            # Instead, copy the file to output (if desired to move/copy it)
            dest_path = f'output/{img_path.split("/")[-1]}'  # Customize destination path as needed
            with open(img_path, 'rb') as img_file:
                with open(dest_path, 'wb') as output_file:
                    shutil.copyfileobj(img_file, output_file)