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
Python-Assignment/
├── file_loader/
│   ├── file_loader.py         # Abstract class for file loading
│   ├── pdf_loader.py          # Class for loading and processing PDF files
│   ├── docx_loader.py         # Class for loading and processing DOCX files
│   └── ppt_loader.py          # Class for loading and processing PPT files
├── data_extractor/
│   └── data_extractor.py      # Class for extracting text, images, tables, and links
├── storage/
│   ├── file_storage.py        # Class for saving data to files (text, images, tables)
│   ├── sql_storage.py         # Class for storing data in an SQL database
│   └── storage.py             # Abstract class for storage handling
├── tests/                     # Directory containing test files (PDF, DOCX, PPT) for testing
├── output/                    # Directory where extracted files will be stored
├── main.py                    # Script for running the tests and extraction
└── README.md                  # Project documentation (this file)
```

## Installation
- Clone the repo:
```
git clone  https://github.com/PalakpreetKaurShorthillsAI/Assignment-Python.git

cd Assignment-Python.git
```
- Set up a Python virtual environment and install dependencies:
```
python -m venv env
source env/bin/activate   
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
- PDF - Loader, Text Extraction, Link Extraction, Table Extraction, Metadata Extraction, Storage
- DOCX: Loader, Text Extraction, Link Extraction, Table Extraction, Metadata Extraction, Storage
- PPTX: Loader, Text Extraction, Link Extraction, Table Extraction, Metadata Extraction, Storage
  
## Unit Testing
Unit tests are planned to cover the following aspects:
- File validation and loading
- Text extraction
- Hyperlink extraction
- Image Extraction
- Table extraction
- MySQL data storage

  

