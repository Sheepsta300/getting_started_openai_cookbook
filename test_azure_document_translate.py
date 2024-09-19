import os
import unittest
from azure_document_translation_tool import AzureDocumentTranslateTool


class TestAzureDocumentTranslateTool(unittest.TestCase):

    def setUp(self):
        # Initialize the AzureDocumentTranslateTool with hardcoded values
        self.tool = AzureDocumentTranslateTool(
            text_translation_key="your_key_here",
            text_translation_region="your_region_here",
            text_translation_endpoint="https://your_endpoint_here"
        )


    def test_initialization(self):
        """Test if the tool is initialized with the correct parameters."""
        self.assertIsNotNone(self.tool.client, "Client should be initialized.")

    def test_translate_text(self):
        """Test the translate_text method."""
        translated_text = self.tool.translate_text("my name is hello", "es")
        self.assertEqual(translated_text, "mi nombre es hola")

    def test_read_text_from_file(self):
        """Test the read_text_from_file method."""
        text = self.tool.read_text_from_file("test.txt")
        self.assertEqual(text, "The text in test.txt")


if __name__ == "__main__":
    unittest.main()
