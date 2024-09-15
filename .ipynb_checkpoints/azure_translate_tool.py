from typing import Optional

from langchain_core.tools import BaseTool
from langchain_core.pydantic_v1 import root_validator
from langchain_core.utils import get_from_dict_or_env
from langchain_core.callbacks import CallbackManagerForToolRun
import os
import requests
import logging

logger = logging.getLogger(__name__)

class AzureTranslateTool(BaseTool):
    """Tool that queries the Azure Cognitive Services Translator API.

    This tool is designed to translate text using the Azure Translator API from Azure Cognitive Services.
    """

    azure_cogs_key: str = ""  #: :meta private:
    azure_cogs_region: str = ""  #: :meta private:
    translator_endpoint: str = ""  #: :meta private:

    name: str = "azure_cognitive_services_translator"
    description: str = (
        "A wrapper around Azure Cognitive Services Translator. "
        "Useful for translating text between languages."
    )

    @root_validator(pre=True)
    def validate_environment(cls, values):
        """Validate that API key, region, and endpoint exist in the environment."""
        azure_cogs_key = get_from_dict_or_env(values, "azure_cogs_key", "AZURE_OPENAI_TRANSLATE_API_KEY")
        azure_cogs_region = get_from_dict_or_env(values, "azure_cogs_region", "REGION")
        translator_endpoint = get_from_dict_or_env(
            values, "translator_endpoint", "AZURE_OPENAI_TRANSLATE_ENDPOINT",
            "https://api.cognitive.microsofttranslator.com/"
        )

        if not azure_cogs_key or not azure_cogs_region:
            raise ValueError("Missing API key or region in environment variables")

        values["azure_cogs_key"] = azure_cogs_key
        values["azure_cogs_region"] = azure_cogs_region
        values["translator_endpoint"] = translator_endpoint
        return values

    @classmethod
    def from_env(cls, use_document_translation=False):
        """Create an instance of the tool using environment variables."""
        azure_cogs_key = os.getenv("AZURE_OPENAI_TRANSLATE_API_KEY")
        azure_cogs_region = os.getenv("REGION")
        translator_endpoint = "https://api.cognitive.microsofttranslator.com/"

        if not azure_cogs_key or not azure_cogs_region:
            raise ValueError("Missing API key or region in environment variables")

        return cls(azure_cogs_key=azure_cogs_key, azure_cogs_region=azure_cogs_region, translator_endpoint=translator_endpoint)

    def _translate_text(self, text: str, to_language: str) -> str:
        """Translate text using the Azure Translator API."""
        if not text:
            raise ValueError("Text for translation is empty.")

        path = '/translate?api-version=3.0'
        constructed_url = self.translator_endpoint + path
        headers = {
            'Ocp-Apim-Subscription-Key': self.azure_cogs_key,
            'Ocp-Apim-Subscription-Region': self.azure_cogs_region,
            'Content-type': 'application/json',
        }
        body = [{'text': text}]
        params = {'to': to_language}

        response = requests.post(constructed_url, headers=headers, json=body, params=params)
        response_json = response.json()

        if response.status_code == 200:
            translated_text = response_json[0]['translations'][0]['text']
            return translated_text
        else:
            logger.error(f"Translation failed with status code {response.status_code}: {response_json}")
            raise RuntimeError(f"Error during translation: {response_json}")

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Run the tool to perform translation."""
        try:
            to_language = "fr"  # Default to French translation
            translated_text = self._translate_text(query, to_language)
            return translated_text
        except Exception as e:
            logger.error(f"Error while running AzureTranslateTool: {e}")
            raise RuntimeError(f"Error while running AzureTranslateTool: {e}")


# Example usage
if __name__ == "__main__":
    tool = AzureTranslateTool.from_env()
    translated_text = tool._run("does this work")
    print(f"Translated text: {translated_text}")
