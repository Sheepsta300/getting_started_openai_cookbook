from __future__ import annotations
import logging
import os
from typing import Any, Dict, Optional
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import root_validator
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
import requests

logger = logging.getLogger(__name__)


class AzureTranslateTool(BaseTool):
    """Tool that queries the Azure Cognitive Services Translator API.

    This tool is designed to translate text using the Azure Cognitive Services Translator API.
    To set this up, follow instructions at:
    https://learn.microsoft.com/en-us/azure/ai-services/translator/quickstart-text-rest-api?tabs=python
    """

    azure_cogs_key: str
    azure_cogs_region: str
    translator_endpoint: str

    name: str = "azure_cognitive_services_translator"
    description: str = (
        "A wrapper around Azure Cognitive Services Translator. "
        "Useful for translating text between languages."
    )

    # using pre loaded enviroment variables for the API key and region - having trouble accessing the point with os.getenv

    @root_validator(pre=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that API key, region, and endpoint exist in the environment."""
        values["azure_cogs_key"] = os.getenv("AZURE_OPENAI_TRANSLATE_API_KEY")
        values["azure_cogs_region"] = os.getenv("REGION")
        values["translator_endpoint"] = os.getenv("AZURE_OPENAI_TRANSLATE_ENDPOINT",
                                                  "https://api.cognitive.microsofttranslator.com/")
        if not values["azure_cogs_key"] or not values["azure_cogs_region"] or not values["translator_endpoint"]:
            raise ValueError("Missing environment variables for Azure Translator API")

        return values

    def _translate_text(self, text: str, to_language: str) -> str:
        """Translate text using the Azure Translator API."""
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
            translated_text = self._translate_text(query, "en")  # Default target language is English
            return translated_text
        except Exception as e:
            raise RuntimeError(f"Error while running AzureTranslateTool: {e}")
