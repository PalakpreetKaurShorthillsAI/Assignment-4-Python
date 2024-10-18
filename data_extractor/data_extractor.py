import os
import pdfplumber
import docx
from pptx import Presentation
from PIL import Image
import io
from abc import ABC, abstractmethod
 
 
# Base DataExtractor class
class DataExtractor(ABC):
    def __init__(self, file_loader):
        self.file_loader = file_loader
        self.content = file_loader.load_file()
 
    def get_file_name(self):
        """Return the base name of the file being processed."""
        return os.path.basename(self.file_loader.file_path)
 
    def save_image(self, img_data, index, file_ext, page_number=None):
        """Save the image data and return its path."""
        img_filename = f"{self.get_file_name().replace(file_ext, '')}_img_{index}.png"
        if page_number is not None:
            img_filename = f"{self.get_file_name().replace(file_ext, '')}_page_{page_number + 1}_img_{index}.png"
        img_path = os.path.join('output', img_filename)
        image = Image.open(io.BytesIO(img_data))
        image.save(img_path)
        return img_path
 
    @abstractmethod
    def extract_text(self):
        pass
 
    @abstractmethod
    def extract_tables(self):
        pass
 
    @abstractmethod
    def extract_images(self):
        pass
 
    @abstractmethod
    def extract_metadata(self):
        pass
 
    @abstractmethod
    def extract_links(self):
        pass
 
 
# PDFDataExtractor class
class PDFDataExtractor(DataExtractor):
    def __init__(self, loader):
        super().__init__(loader)
        self.pdf = None
        self.load_pdf()
 
    def load_pdf(self):
        self.pdf = pdfplumber.open(self.file_loader.file_path)
 
    def extract_text(self):
        text = ""
        if self.pdf:
            for page in self.pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
 
    def extract_tables(self):
        tables = []
        if self.pdf:
            for page in self.pdf.pages:
                tables.extend(page.extract_tables())
        return tables
 
    def extract_images(self):
        images = []
        if self.pdf:
            for page_number, page in enumerate(self.pdf.pages):
                for img_index, img in enumerate(page.images):
                    if 'stream' in img:
                        img_data = img['stream'].get_rawdata()
                        img_path = self.save_image(img_data, img_index + 1, '.pdf', page_number)
                        images.append(img_path)
        return images
 
    def extract_metadata(self):
        return self.pdf.metadata if self.pdf else {}
 
    def extract_links(self):
        links = []
        if self.pdf:
            for page in self.pdf.pages:
                if hasattr(page, 'annots') and page.annots:
                    for annot in page.annots:
                        uri = annot.get("uri")
                        if uri:
                            links.append(uri)
        return links
 
    def close_pdf(self):
        if self.pdf:
            self.pdf.close()
 
 
# DOCXDataExtractor class
class DOCXDataExtractor(DataExtractor):
    def extract_text(self):
        text = ""
        doc = docx.Document(self.file_loader.file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text.strip()
 
    def extract_tables(self):
        tables = []
        doc = docx.Document(self.file_loader.file_path)
        for table in doc.tables:
            table_data = []
            for row in table.rows:
                row_data = [cell.text for cell in row.cells]
                table_data.append(row_data)
            tables.append(table_data)
        return tables
 
    def extract_images(self):
        images = []
        doc = docx.Document(self.file_loader.file_path)
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                img_data = rel.target_part.blob
                img_path = self.save_image(img_data, len(images) + 1, '.docx')
                images.append(img_path)
        return images
 
    def extract_metadata(self):
        doc = docx.Document(self.file_loader.file_path)
        return doc.core_properties
 
    def extract_links(self):
        links = []
        doc = docx.Document(self.file_loader.file_path)
        for rel in doc.part.rels.values():
            if "hyperlink" in rel.reltype:
                links.append(rel.target_ref)
        return links
 
 
# PPTDataExtractor class
class PPTDataExtractor(DataExtractor):
    def extract_text(self):
        text = ""
        prs = Presentation(self.file_loader.file_path)
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
        return text.strip()
 
    def extract_tables(self):
        # Assuming tables are stored in shapes
        tables = []
        # You can add table extraction logic here for PPT
        return tables
 
    def extract_images(self):
        images = []
        prs = Presentation(self.file_loader.file_path)
        for slide_number, slide in enumerate(prs.slides):
            for shape_index, shape in enumerate(slide.shapes):
                if shape.shape_type == 13:  # Check if the shape is a picture
                    img_data = shape.image.blob
                    img_path = self.save_image(img_data, shape_index + 1, '.pptx', slide_number)
                    images.append(img_path)
        return images
 
    def extract_metadata(self):
        prs = Presentation(self.file_loader.file_path)
        return prs.core_properties
 
    def extract_links(self):
        links = set()  # Use a set to store unique links
        prs = Presentation(self.file_loader.file_path)
        for slide in prs.slides:
            for shape in slide.shapes:
                if shape.has_text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                            if run.hyperlink:
                                links.add(run.hyperlink.address)
        return list(links)
 