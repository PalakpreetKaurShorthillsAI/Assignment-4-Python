import unittest
from unittest.mock import MagicMock, patch

# Import your classes using the correct paths
from file_loader import PDFLoader, DOCXLoader, PPTLoader
from data_extractor.data_extractor import DataExtractor
from storage.file_storage import FileStorage
from storage.sql_storage import SQLStorage

class TestFileLoaders(unittest.TestCase):

    def setUp(self):
        self.pdf_loader = PDFLoader("test.pdf")
        self.docx_loader = DOCXLoader("test.docx")
        self.ppt_loader = PPTLoader("test.pptx")

    # PDF Loader Tests
    def test_pdf_loader_valid(self):
        self.pdf_loader.load = MagicMock(return_value=True)
        self.assertTrue(self.pdf_loader.load())

    def test_pdf_loader_invalid(self):
        self.pdf_loader.load = MagicMock(side_effect=FileNotFoundError)
        with self.assertRaises(FileNotFoundError):
            self.pdf_loader.load()

    def test_pdf_loader_empty_file(self):
        self.pdf_loader.load = MagicMock(return_value=False)
        self.assertFalse(self.pdf_loader.load())

    # DOCX Loader Tests
    def test_docx_loader_valid(self):
        self.docx_loader.load = MagicMock(return_value=True)
        self.assertTrue(self.docx_loader.load())

    def test_docx_loader_invalid(self):
        self.docx_loader.load = MagicMock(side_effect=FileNotFoundError)
        with self.assertRaises(FileNotFoundError):
            self.docx_loader.load()

    def test_docx_loader_empty_file(self):
        self.docx_loader.load = MagicMock(return_value=False)
        self.assertFalse(self.docx_loader.load())

    # PPT Loader Tests
    def test_ppt_loader_valid(self):
        self.ppt_loader.load = MagicMock(return_value=True)
        self.assertTrue(self.ppt_loader.load())

    def test_ppt_loader_invalid(self):
        self.ppt_loader.load = MagicMock(side_effect=FileNotFoundError)
        with self.assertRaises(FileNotFoundError):
            self.ppt_loader.load()

    def test_ppt_loader_empty_file(self):
        self.ppt_loader.load = MagicMock(return_value=False)
        self.assertFalse(self.ppt_loader.load())

    # Additional tests for file format validity
    def test_pdf_loader_not_a_pdf(self):
        self.pdf_loader.load = MagicMock(side_effect=ValueError("Not a PDF"))
        with self.assertRaises(ValueError):
            self.pdf_loader.load()

    def test_docx_loader_not_a_docx(self):
        self.docx_loader.load = MagicMock(side_effect=ValueError("Not a DOCX"))
        with self.assertRaises(ValueError):
            self.docx_loader.load()

    def test_ppt_loader_not_a_pptx(self):
        self.ppt_loader.load = MagicMock(side_effect=ValueError("Not a PPTX"))
        with self.assertRaises(ValueError):
            self.ppt_loader.load()


class TestDataExtractor(unittest.TestCase):

    def setUp(self):
        self.pdf_loader = PDFLoader("test.pdf")
        self.data_extractor = DataExtractor(self.pdf_loader)

        # Mocking the methods in PDFLoader for testing
        self.pdf_loader.extract_text = MagicMock(return_value=[{"text": "Sample Text", "metadata": {"page": 1}}])
        self.pdf_loader.extract_links = MagicMock(return_value=[{"text": "link", "url": "http://example.com", "page": 1}])
        self.pdf_loader.extract_images = MagicMock(return_value=[{"resolution": "1920x1080", "format": "JPEG", "page": 1}])
        self.pdf_loader.extract_tables = MagicMock(return_value=[{"dimensions": (3, 4), "page": 1}])

    # Text extraction tests
    def test_extract_text(self):
        text_data = self.data_extractor.extract_text()
        self.assertEqual(len(text_data), 1)
        self.assertEqual(text_data[0]["text"], "Sample Text")
        self.assertEqual(text_data[0]["metadata"]["page"], 1)

    def test_extract_text_empty(self):
        self.pdf_loader.extract_text = MagicMock(return_value=[])
        text_data = self.data_extractor.extract_text()
        self.assertEqual(len(text_data), 0)

    # Link extraction tests
    def test_extract_links(self):
        links_data = self.data_extractor.extract_links()
        self.assertEqual(len(links_data), 1)
        self.assertEqual(links_data[0]["text"], "link")
        self.assertEqual(links_data[0]["url"], "http://example.com")
        self.assertEqual(links_data[0]["page"], 1)

    def test_extract_links_empty(self):
        self.pdf_loader.extract_links = MagicMock(return_value=[])
        links_data = self.data_extractor.extract_links()
        self.assertEqual(len(links_data), 0)

    # Image extraction tests
    def test_extract_images(self):
        images_data = self.data_extractor.extract_images()
        self.assertEqual(len(images_data), 1)
        self.assertEqual(images_data[0]["resolution"], "1920x1080")
        self.assertEqual(images_data[0]["format"], "JPEG")

    def test_extract_images_empty(self):
        self.pdf_loader.extract_images = MagicMock(return_value=[])
        images_data = self.data_extractor.extract_images()
        self.assertEqual(len(images_data), 0)

    # Table extraction tests
    def test_extract_tables(self):
        tables_data = self.data_extractor.extract_tables()
        self.assertEqual(len(tables_data), 1)
        self.assertEqual(tables_data[0]["dimensions"], (3, 4))
        self.assertEqual(tables_data[0]["page"], 1)

    def test_extract_tables_empty(self):
        self.pdf_loader.extract_tables = MagicMock(return_value=[])
        tables_data = self.data_extractor.extract_tables()
        self.assertEqual(len(tables_data), 0)

    # Metadata tests for extraction
    def test_extract_text_with_metadata(self):
        self.pdf_loader.extract_text = MagicMock(return_value=[{"text": "Header", "metadata": {"page": 2, "font": "Arial"}}])
        text_data = self.data_extractor.extract_text()
        self.assertEqual(text_data[0]["metadata"]["font"], "Arial")

    def test_extract_links_with_invalid_url(self):
        self.pdf_loader.extract_links = MagicMock(return_value=[{"text": "bad link", "url": None, "page": 1}])
        links_data = self.data_extractor.extract_links()
        self.assertIsNone(links_data[0]["url"])


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        self.file_storage = FileStorage("output_directory")
        self.data_extractor = MagicMock()

    @patch("os.path.exists", return_value=True)  # Mocking file existence for testing
    def test_save_images(self, mock_exists):
        self.data_extractor.images = [{"resolution": "1920x1080", "format": "JPEG", "page": 1}]
        self.file_storage.save_images = MagicMock(return_value=True)
        result = self.file_storage.save_images(self.data_extractor)
        self.assertTrue(result)  # Assuming save_images returns True on success

    @patch("os.path.exists", return_value=True)
    def test_save_tables(self, mock_exists):
        self.data_extractor.tables = [{"dimensions": (3, 4), "page": 1}]
        self.file_storage.save_tables = MagicMock(return_value=True)
        result = self.file_storage.save_tables(self.data_extractor)
        self.assertTrue(result)  # Assuming save_tables returns True on success

    # Test saving images with no images
    def test_save_images_empty(self):
        self.data_extractor.images = []
        self.file_storage.save_images = MagicMock(return_value=True)
        result = self.file_storage.save_images(self.data_extractor)
        self.assertTrue(result)

    # Test saving tables with no tables
    def test_save_tables_empty(self):
        self.data_extractor.tables = []
        self.file_storage.save_tables = MagicMock(return_value=True)
        result = self.file_storage.save_tables(self.data_extractor)
        self.assertTrue(result)

    # Testing handling of incorrect formats
    def test_save_images_incorrect_format(self):
        self.data_extractor.images = [{"resolution": "1920x1080", "format": "EXE", "page": 1}]
        with self.assertRaises(ValueError):
            self.file_storage.save_images(self.data_extractor)

    def test_save_tables_incorrect_format(self):
        self.data_extractor.tables = [{"dimensions": (3, 4), "page": 1, "format": "TXT"}]
        with self.assertRaises(ValueError):
            self.file_storage.save_tables(self.data_extractor)


class TestSQLStorage(unittest.TestCase):

    def setUp(self):
        self.sql_storage = SQLStorage("test_database")
        self.data_extractor = MagicMock()

    def test_store_data(self):
        self.data_extractor.texts = ["Sample Text"]
        self.data_extractor.links = [{"text": "link", "url": "http://example.com"}]
        self.sql_storage.store_data = MagicMock(return_value=True)
        result = self.sql_storage.store_data(self.data_extractor)
        self.assertTrue(result)

    def test_store_data_empty(self):
        self.data_extractor.texts = []
        self.data_extractor.links = []
        self.sql_storage.store_data = MagicMock(return_value=True)
        result = self.sql_storage.store_data(self.data_extractor)
        self.assertTrue(result)

    @patch("src.storage.sql_storage.connect", side_effect=Exception("DB Connection Error"))
    def test_store_data_db_connection_error(self, mock_connect):
        self.data_extractor.texts = ["Sample Text"]
        with self.assertRaises(Exception):
            self.sql_storage.store_data(self.data_extractor)

    def test_store_data_invalid_text_format(self):
        self.data_extractor.texts = ["Sample Text", None]
        with self.assertRaises(ValueError):
            self.sql_storage.store_data(self.data_extractor)

    def test_store_data_invalid_link_format(self):
        self.data_extractor.links = [{"text": "link", "url": None}]
        with self.assertRaises(ValueError):
            self.sql_storage.store_data(self.data_extractor)

    # Test storing large amounts of data
    def test_store_large_amounts_of_data(self):
        self.data_extractor.texts = ["Sample Text"] * 1000  # Mock large dataset
        self.data_extractor.links = [{"text": "link", "url": f"http://example{i}.com"} for i in range(1000)]
        self.sql_storage.store_data = MagicMock(return_value=True)
        result = self.sql_storage.store_data(self.data_extractor)
        self.assertTrue(result)

    # Test storing invalid data formats
    def test_store_data_with_invalid_texts(self):
        self.data_extractor.texts = ["Valid Text", "", None]
        with self.assertRaises(ValueError):
            self.sql_storage.store_data(self.data_extractor)

    def test_store_data_with_invalid_links(self):
        self.data_extractor.links = [{"text": "valid", "url": "http://example.com"}, {"text": None, "url": "http://example.com"}]
        with self.assertRaises(ValueError):
            self.sql_storage.store_data(self.data_extractor)

    # Additional tests for verifying the database state
    def test_store_data_confirms_entry(self):
        self.data_extractor.texts = ["Sample Text"]
        self.data_extractor.links = [{"text": "link", "url": "http://example.com"}]
        self.sql_storage.store_data = MagicMock(return_value=True)
        result = self.sql_storage.store_data(self.data_extractor)
        self.assertTrue(result)
        # Assuming a method exists to verify entries in the database
        self.assertTrue(self.sql_storage.verify_entry("Sample Text"))

    def test_store_data_incorrect_entry(self):
        self.data_extractor.texts = ["Fake Text"]
        self.data_extractor.links = [{"text": "link", "url": "http://example.com"}]
        self.sql_storage.store_data = MagicMock(return_value=False)
        result = self.sql_storage.store_data(self.data_extractor)
        self.assertFalse(result)

    # Test handling of duplicate entries
    def test_store_data_duplicate_entry(self):
        self.data_extractor.texts = ["Duplicate Text"]
        self.sql_storage.store_data = MagicMock(side_effect=Exception("Duplicate Entry"))
        with self.assertRaises(Exception):
            self.sql_storage.store_data(self.data_extractor)

    # Mocking a function to count entries
    def test_count_entries(self):
        self.sql_storage.count_entries = MagicMock(return_value=10)
        count = self.sql_storage.count_entries()
        self.assertEqual(count, 10)

if __name__ == '__main__':
    # Run tests with verbose output
    suite = unittest.TestLoader().discover(start_dir='.', pattern="*.py")

    # Use TextTestRunner to get a detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary of results
    print(f"\nTotal Tests Run: {result.testsRun}")
    print(f"Tests Passed: {len(result.successes)}")
    print(f"Tests Failed: {len(result.failures)}")
    print(f"Tests Errored: {len(result.errors)}")
