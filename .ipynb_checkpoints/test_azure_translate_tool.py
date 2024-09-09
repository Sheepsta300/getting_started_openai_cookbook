import unittest
from unittest.mock import patch
from azure_translate_tool import AzureTranslateTool

class TestAzureTranslateTool(unittest.TestCase):

    @patch('azure_translate_tool.requests.post')
    def test_translate_text_success(self, mock_post):
        mock_response = {
            'translations': [
                {'text': 'Bonjour'}
            ]
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = [mock_response]

        tool = AzureTranslateTool(
            azure_cogs_key="fake-key",
            azure_cogs_region="fake-region",
            translator_endpoint="https://api.cognitive.microsofttranslator.com"
        )

        result = tool._translate_text("Hello", "fr")
        self.assertEqual(result, "Bonjour")

    @patch('azure_translate_tool.requests.post')
    def test_translate_text_failure(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {'error': {'message': 'Bad request'}}

        tool = AzureTranslateTool(
            azure_cogs_key="fake-key",
            azure_cogs_region="fake-region",
            translator_endpoint="https://api.cognitive.microsofttranslator.com"
        )

        with self.assertRaises(RuntimeError):
            tool._translate_text("Hello", "fr")


if __name__ == '__main__':
    unittest.main()
