# Azure AI Vision
[Azure AI Vision](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/) is an cloud-based API service to **process images** and return **information on visual features** user is interested in using its **pre-built models** that are ready to use. The service is divided into 4 main subgroups.

## Subgroups of Azure AI Vision
|   | Group  | Description | Client SDK | LangChain Integration |
|:-:|:--------|:------------|:---|:-----|
| 1 | Optical Character Recognition service ([OCR](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview-ocr))  | Extracts text from images. | [sdk/cognitiveservices/azure-cognitiveservices-vision-computervision](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/cognitiveservices/azure-cognitiveservices-vision-computervision) | confusing... couldnt find like direct integration, and blury regarding how ocr is used in ai document intelligence etc... |
| 2 | [Image Analysis](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview-image-analysis?tabs=4-0) | Extracts visual features from images | [sdk/vision/azure-ai-vision-imageanalysis](https://github.com/Azure/azure-sdk-for-python/tree/azure-ai-vision-imageanalysis_1.0.0b3/sdk/vision/azure-ai-vision-imageanalysis)  | Azure AI Service Toolkit |
| 3 | [Face](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview-identity) | Face Recognition | [sdk/face/azure-ai-vision-face](https://github.com/Azure/azure-sdk-for-python/tree/azure-ai-vision-imageanalysis_1.0.0b3/sdk/face/azure-ai-vision-face) |  Can't find anything... |
| 4 | [Video Analysis](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/intro-to-spatial-analysis-public-preview?tabs=sa) | [Spatial Analysis](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/intro-to-spatial-analysis-public-preview?tabs=sa#spatial-analysis) and [Video Retrieval](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/intro-to-spatial-analysis-public-preview?tabs=sa#video-retrieval) | [preview only?](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/spatial-analysis-container?tabs=azure-stack-edge) / [preview only?](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/how-to/video-retrieval) | Not available yet? I was looking forward to this |


## Integrating with LangChain
LangChain offers `toolkits` to interact with external `Azure AI Services API` and `Azure Cognitive Services API`. 


### 1. [Azure AI Services Toolkit](https://python.langchain.com/v0.2/docs/integrations/tools/azure_ai_services/)
The tools bundled in this toolkit are:
| langchain tool class | package/class | link to services/subgroups|
|-|--------|----------|
| AzureAiServicesDocumentIntelligenceTool() | azure.ai.formrecognizer DocumentAnalysisClient  | Azure AI Document Intelligence |
| **AzureAiServicesImageAnalysisTool()** |  azure.ai.vision.imageanalysis ImageAnalysisClient / models.VisualFeatures | **Azure AI Vision/Image Analysis** |
| AzureAiServicesSpeechToTextTool() |  azure.cognitiveservices.speech | Azure AI Speech/Speach to text? |
| AzureAiServicesTextToSpeechTool() |  azure.cognitiveservices.speech | Azure AI Speech/Text to speach? | 
| AzureAiServicesTextAnalyticsForHealthTool() | azure.ai.textanalytics | is it under Azure AI Speech? [Azure Cognitive Services](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/textanalytics/Azure.AI.TextAnalytics/README.md) |

### 2. [Azure Cognitive Services Toolkit](https://python.langchain.com/v0.2/docs/integrations/tools/azure_cognitive_services/) 
| langchain tool class | package/class | link to services/subgroups|
|-|--------|----------|
| AzureCogsFormRecognizerTool() | azure.ai.formrecognizer [DocumentAnalysisClient](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/formrecognizer/azure-ai-formrecognizer/azure/ai/formrecognizer/_document_analysis_client.py)  | [Azure AI Document Intelligence](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/?view=doc-intel-4.0.0) family group? |
| AzureCogsSpeech2TextTool() |  
| AzureCogsText2SpeechTool() |   
| AzureCogsTextAnalyticsHealthTool() |   

# Azure AI Custom Vision

# LangChain's Azure AI Github Issues

## My Q&A
### ❓Azure AI Vision v.s. Azure AI Custom Vision
The key difference is Azure AI Vision uses pre-built models that are ready to use _v.s._ [Azure AI Custom Vision]() allows users to upload their own images and manually annotate them to train their own custom vision models.

### ❓Azure AI Services Toolkit v.s. Azure Cognitive Services Toolkit
The difference between them is ...  Is Cognitive Services an older version and AI Services the newer one or something else?

[As of July 2023, Azure AI services encompass all of what were previously known as Cognitive Services and Azure Applied AI Services.](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview?view=doc-intel-4.0.0)

### ❓OpenAI's AzureOpenAI() v.s. langchain_openai's AzureOpenAI()












