import os
import logging
from typing import Optional
from azure.ai.translation.text.models import InputTextItem
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient
from langchain_community.document_loaders import TextLoader
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun

logger = logging.getLogger(__name__)


class AzureDocumentTranslateTool(BaseTool):
    """
    A tool that uses Azure Text Translation API to translate a text document from
    any language into a target language.
    """

    text_translation_key: str = ""  #: :meta private:
    text_translation_region: str = ""  #: :meta private:
    text_translation_endpoint: str = ""  #: :meta private:
    client: Optional[TextTranslationClient] = None  # Declare client here

    name: str = "azure_document_translate_tool"
    description: str = (
        """
        This tool can be used if you want to translate a document into a specific language.
        The document has to be a text document.
        """
    )

    def __init__(self, *,
                 text_translation_key: Optional[str] = None,
                 text_translation_region: Optional[str] = None,
                 text_translation_endpoint: Optional[str] = None
                 ) -> None:
        # Initialize parent class
        super().__init__()

        # Use provided values or fall back to environment variables
        self.text_translation_key = text_translation_key or os.getenv("TEXT_TRANSLATION_KEY")
        self.text_translation_region = text_translation_region or os.getenv("TEXT_TRANSLATION_REGION")
        self.text_translation_endpoint = text_translation_endpoint or os.getenv("TEXT_TRANSLATION_ENDPOINT")

        if not all([self.text_translation_key, self.text_translation_region, self.text_translation_endpoint]):
            raise ValueError("Azure Cognitive Services key, region, and endpoint must be provided")

        try:
            # Initialize the TextTranslationClient
            self.client = TextTranslationClient(
                endpoint=self.text_translation_endpoint,
                credential=AzureKeyCredential(self.text_translation_key)
            )
            logger.info("TextTranslationClient initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize TextTranslationClient: {e}")
            raise

    def read_text_from_file(self, file_path: str) -> str:
        """Read and return text from a text file using LangChain's TextLoader."""
        # Initialize the TextLoader with the file path
        loader = TextLoader(file_path)
        document = loader.load()  # This will be a list with one document

        # Check if there is at least one document
        if document:
            text = document[0].page_content  # Get the content of the first document
        else:
            text = ""  # Handle the case where the document list is empty
        return text

    def translate_text(self, text: str, target_language: str) -> str:
        """Translate text using Azure's document Translation API."""
        try:
            # Prepare the request body
            request_body = [InputTextItem(text=text)]

            # Perform the translation
            response = self.client.translate(
                content=request_body,
                to=[target_language]  # List of target languages
            )

            # Extract the translated text from the response
            translations = response[0].translations
            if translations:
                translated_text = translations[0].text
            else:
                translated_text = ""  # Handle the case where no translations are returned

            return translated_text
        except Exception as e:
            logger.error(f"Error occurred during translation: {e}")
            raise

    def _run(self, query: str, target_language: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """"Run the tool"""
        try:
            return self.translate_text(query, target_language)
        except Exception as e:
            logger.error(f"Error while running AzureDocumentTranslateTool: {e}")
            raise RuntimeError(f"Error while running AzureDocumentTranslateTool: {e}")
