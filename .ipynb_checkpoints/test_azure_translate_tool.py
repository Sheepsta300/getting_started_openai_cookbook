import os
import unittest
from azure_translate_tool import AzureTranslateTool

class TestAzureTranslateTool(unittest.TestCase):

    def setUp(self):
        #using pre loaded enviroment variables for the API key and region - having trouble accessing the point with os.getenv

        self.azure_translate_tool = AzureTranslateTool(
            azure_cogs_key=os.getenv("AZURE_OPENAI_TRANSLATE_API_KEY"),
            azure_cogs_region=os.getenv("REGION"),
            translator_endpoint="https://api.cognitive.microsofttranslator.com"
        )

    def test_translate_text_success(self):
        """Test for successful translation using valid text and languages."""
        try:
            result = self.azure_translate_tool._translate_text("Hello", "fr")
            self.assertEqual(result, "Bonjour")
        except Exception as e:
            self.fail(f"Translation failed with an error: {str(e)}")

    def test_translate_text_failure(self):
        """Test for failure when using invalid input."""
        with self.assertRaises(RuntimeError):
            self.azure_translate_tool._translate_text("", "fr")  # Invalid input test

if __name__ == '__main__':
    unittest.main()
