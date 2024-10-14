# Assignment-4-Python
This project provides a Python solution to extract text, hyperlinks, images, and tables from PDF, DOCX, and PPTX files while capturing metadata such as file type. The project also includes functionality to store the extracted data in both files and a MySQL database.
## Features
- Text Extraction: Extracts plain text from PDF, DOCX, and PPTX files along with metadata (font style, page number, slide number, headings).
- Hyperlink Extraction: Extracts URLs and linked text from PDF, DOCX, and PPTX files.
- Image Extraction: Extracts images and metadata (resolution, format, page/slide number) and stores them in separate folders.
- Table Extraction: Extracts tables and stores them in CSV format for each file type.
- Storage Options:
  - File Storage: Saves text, links, images, and tables into separate files.
  - SQL Storage: Stores extracted data into a MySQL database.

## Requirements
<ul>
<li>PyMuPDF: For handling PDFs.</li>
<li>Camelot: For extracting tables from PDFs.</li>
<li>python-docx: For handling DOCX files.</li>
<li>python-pptx: For handling PPTX files.</li>
<li>OpenCV: Required for Camelot table extraction.</li>
<li>Ghostscript: Required for PDF handling in Camelot.</li>
<li>Pandas: Used for managing table data.</li> </ul>


## Project Structure 
```
├── loaders
│   ├── file_loader.py       # Abstract base class for file loaders
│   ├── pdf_loader.py        # PDF loader implementation
│   └── docx_loader.py       # DOCX loader implementation
│   └── pptx_loader.py       # PPTX loader implementation
├── extractors
│   └── data_extract.py      # Data extraction logic for text, images, URLs, and tables
├── storage
│   └── file_storage.py      # Handles saving extracted data to files
├── tests
│   └── test_extractor.py    # Unit tests for the extractors
├── requirements.txt         # Dependencies
└── README.md                # Project documentation
|-- test_files/              # Test files (PDF, DOCX, PPTX) used for manual and unit testing
    |-- pdf/
    |-- docx/
    |-- pptx/

```

## Installation
- Clone the repo:
```
git clone  https://github.com/PalakpreetKaurShorthillsAI/Assignment-4-Python.git

cd Assignment-4-Python.git
```
- Set up a Python virtual environment and install dependencies:
```
python -m venv env
source env/bin/activate   # On Windows use `env\Scripts\activate`
pip install -r requirements.txt
```
- Set up your MySQL database and create a .env file for MySQL credentials:
```
DB_HOST=your_host
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database
```
## Usage
- Run the main script:
```
python3 main.py
```
- The extracted data will be saved in the output/ folder and organized into subfolders based on file type (PDF, DOCX, PPTX). Additionally, data will be stored in the MySQL database if configured correctly.
## Manual Testing
Test cases have been manually prepared and provided in the Excel file and can be tested with different file types and scenarios:
- PDF: Small, large, corrupted PDFs.
- DOCX: Small, large, corrupted DOCX files.
- PPTX: Small, large, corrupted PPTX files.
## Unit Testing
Unit tests are planned to cover the following aspects:
- File validation and loading
- Text extraction
- Hyperlink extraction
- Image Extraction
- Table extraction
- MySQL data storage

  
To run unit tests: python3 -m unittest tests/test_extractor.py
```
pytest tests/test_extractor.py
```
