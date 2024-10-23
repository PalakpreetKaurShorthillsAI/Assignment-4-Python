import os,io,csv
import docx.document
import pdfplumber
import docx
from pptx import Presentation
from PIL import Image
 
# from data_extractor import UniversalDataExtractor
 
class UniversalDataExtractor():
    def __init__(self,loader):
        self.file_loader = loader
        self.content = self.file_loader.load_file()
        self.file_type = os.path.splitext(loader.file_path)[1].lower()
        
        if self.file_type == '.pdf':
            self.pdf = pdfplumber.open(self.file_loader.file_path)
            
        elif self.file_type == '.docx':
            self.doc = docx.Document(self.file_loader.file_path)
        elif self.file_type == '.pptx':
            self.prs = Presentation(self.file_loader.file_path)
 
    def extract_text(self):
        extracted_data = {'text': '', 'metadata': {}}
 
        # Extract text based on the file type
        if self.file_type == '.pdf':
           
               return "\n".join(page.extract_text() or "" for page in self.pdf.pages).strip()
        
        elif self.file_type == '.docx':
               return  "\n".join(para.text for para in self.doc.paragraphs).strip()
        elif self.file_type == 'pptx':
            text = ''
            for slide in self.prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + "\n"
            return text.strip()
 
        # Return extracted text along with optional metadata
        return ""
 
    
    def extract_tables(self):
        if self.file_type == ".pdf":
            return [table for page in self.pdf.pages for table in page.extract_tables()]
        elif self.file_type == "docx":
            tables =[]
            for table in self.doc.tables:
                table_data = [[cell.text for cell in row.cells] for row in table.rows]
                tables.append(table_data)
            return tables
        elif self.file_type == ".pptx":
            return []
        return []

    
    def extract_images(self):
        images = []
        if self.file_type == ".pdf":
            for page_number, page in enumerate(self.pdf.pages):
                for img_index, img in enumerate(page.images):
                    if 'stream' in img:
                        img_data = img['stream'].get_rawdata()
                        images.append(self.save_image(img_data, img_index+1, ".pdf", page_number))
        elif self.file_type == ".docx":
            for rel in self.doc.part.rels.values():
                if "image" in rel.target_ref:
                    img_data = rel.target_part.blob
                    images.append(self.save_image(img_data, len(images) +1, ".docx"))
 
        elif self.file_type == ".pptx":
            for slide_number, slide in enumerate(self.prs.slides):
                for shape_index, shape in enumerate(slide.shapes):
                    if shape.shape_type == 13:
                        img_data = shape.image.blob
                        images.append(self.save_image(img_data, shape_index +1, ".pptx", slide_number))
        return images
    
    def extract_metadata(self):
        if self.file_type == ".pdf":
            return self.pdf.metadata
        elif self.file_type == ".docx":
            return self.doc.core_properties
        elif self.file_type == ".pptx":
            return self.prs.core_properties
        
        return {}
    
    def extract_links(self):
        links = []
        if self.file_type == ".pdf":
            for page in self.pdf.pages:
                links.extend(annot.get("uri") for annot in getattr(page, 'annots', []) if annot.get("uri"))
 
        elif self.file_type == ".docx":
            for rel in self.doc.part.rels.values():
                if "hyperlink" in rel.reltype:
                    links.append(rel.target_ref)
        
        elif self.file_type == ".pptx":
            for slide in self.prs.slides:
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        for paragraph in shape.text_frame.paragraphs:
                            for run in paragraph.runs:
                                if run.hyperlink:
                                    links.append(run.hyperlink.address)
        return links
    
    def get_file_name(self):
        return os.path.basename(self.file_loader.file_path)
    
    def save_image(self, img_data,index, file_ext, page_number = None):
        img_filename = f"{self.get_file_name().replace(file_ext, '')}_img_{index}.png"
        if page_number is not None:
            img_filename = f"{self.get_file_name().replace(file_ext,'')}_page_{page_number +1}_img_{index}.png"
        img_path = os.path.join('output', img_filename)
        image = Image.open(io.BytesIO(img_data))
        image.save(img_path)
        return img_path
    
    def close(self):
        if self.file_type == '.pdf':
            self.pdf.close()
 