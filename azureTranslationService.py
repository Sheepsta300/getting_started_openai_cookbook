import requests
from langchain_community.document_loaders import TextLoader

# Constants for configuration
FILE_PATH = "replace with your file name"  # Path to your text file
ENDPOINT = "replace with your endpoint"
API_KEY = "replace with your api key"
TARGET_LANGUAGE = "es"  # For Spanish

def read_text_from_file(file_path: str) -> str:
    # Read and return text from a text file using LangChains TextLoader
    loader = TextLoader(file_path)
    document = loader.load()  # This will be a list with one document
    if document:  # Check if there is at least one document
        text = document[0].page_content  # Get the content of the first document
    else:
        text = ""  # Handle the case where the document list is empty
    return text

def translate_text_azure(text: str, endpoint: str, api_key: str, target_language: str) -> str:
    # Translate text from the file using Azure Document Translation API
    url = f"{endpoint}/translate?api-version=3.0&to={target_language}"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Region": "westus2"  # Replace with your region if needed
    }
    body = [{"text": text}]
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()  # Ensure we notice bad responses
    translations = response.json()
    return translations[0]['translations'][0]['text']

def main(file_path: str, endpoint: str, subscription_key: str, target_language: str) -> str:
    # Read, translate, and return the translated text from a file
    # Read text from file
    text = read_text_from_file(file_path)

    # Translate the extracted text
    translated_text = translate_text_azure(text, endpoint, subscription_key, target_language)

    return translated_text

# Example usage
if __name__ == "__main__":
    result = main(FILE_PATH, ENDPOINT, API_KEY, TARGET_LANGUAGE)
    print(result)
