import os
import unittest
from azure_translate_tool import AzureTranslateTool


class TestAzureTranslateTool(unittest.TestCase):

    def setUp(self):
        # Setup AzureTranslateTool with environment-based variables
        self.azure_translate_tool = AzureTranslateTool(
            azure_cogs_key=os.getenv("AZURE_OPENAI_TRANSLATE_API_KEY"),
            azure_cogs_region=os.getenv("REGION"),
            translator_endpoint="https://api.cognitive.microsofttranslator.com"
        )

    def test_translate_text_success(self):
        """Test for successful translation using valid text and languages."""
        try:
            result = self.azure_translate_tool._translate_text("Hello", "fr")
            self.assertIsNotNone(result)  # Ensure we have a result
            self.assertIsInstance(result, str)  # Ensure it's a string
        except Exception as e:
            self.fail(f"Translation failed with an error: {str(e)}")

    def test_translate_text_empty_input(self):
        """Test for failure when using empty input."""
        with self.assertRaises(ValueError):  # Expecting a ValueError for empty input
            self.azure_translate_tool._translate_text("", "fr")

    def test_translate_invalid_language(self):
        """Test for invalid target language code."""
        try:
            self.azure_translate_tool._translate_text("Hello", "xx")  # Invalid language code
        except RuntimeError as e:
            self.assertIn('The target language is not valid', str(e))  # Check error message
        else:
            self.fail("Expected a RuntimeError for invalid language code, but none was raised.")

    def test_missing_env_variables(self):
        """Test for missing environment variables."""
        original_key = os.getenv("AZURE_OPENAI_TRANSLATE_API_KEY")
        original_region = os.getenv("REGION")

        # Temporarily remove the environment variables
        os.environ.pop("AZURE_OPENAI_TRANSLATE_API_KEY", None)
        os.environ.pop("REGION", None)

        # Test if missing variables raises an error
        with self.assertRaises(ValueError):
            AzureTranslateTool.from_env()

        # Restore environment variables
        os.environ["AZURE_OPENAI_TRANSLATE_API_KEY"] = original_key
        os.environ["REGION"] = original_region


if __name__ == '__main__':
    unittest.main()
