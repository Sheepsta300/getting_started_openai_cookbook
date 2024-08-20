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
| AzureAiServicesTextAnalyticsForHealthTool() | azure.ai.textanalytics | Azure AI Language (used be on its own family) |

### ~~2. [Azure Cognitive Services Toolkit](https://python.langchain.com/v0.2/docs/integrations/tools/azure_cognitive_services/)~~ _Its an older version of the service, focus more on the Azure AI Services Toolkit_
The tools bundled in this toolkit are:
| langchain tool class | package/class | link to services/subgroups|
|-|--------|----------|
| AzureCogsFormRecognizerTool() | azure.ai.formrecognizer [DocumentAnalysisClient](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/formrecognizer/azure-ai-formrecognizer/azure/ai/formrecognizer/_document_analysis_client.py)  | [Azure AI Document Intelligence](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/?view=doc-intel-4.0.0) family group? |
| AzureCogsSpeech2TextTool() |  
| AzureCogsText2SpeechTool() |   
| AzureCogsTextAnalyticsHealthTool() |   

### Find Features to Work On
1. **Azure AI Image Analysis: AzureAiServicesImageAnalysisTool - Visual Features missmatch**  
Not all `Visual Features` are available in the langchain tool compared to that of the Azure client sdk. `DENSE_CAPTION`, `SMART_CROPS` and `PEOPLE` are missing in AzureAiServicesImageAnalysisTool?

    - Azure AI Vision Client Python SDK: [sdk/vision/azure-ai-vision-imageanalysis](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/vision/azure-ai-vision-imageanalysis/azure/ai/vision/imageanalysis/models/_enums.py#L13-L34)

        ```python
        class VisualFeatures(str, Enum, metaclass=CaseInsensitiveEnumMeta):
            """The visual features supported by the Image Analysis service."""

            TAGS = "tags"
            """Extract content tags for thousands of recognizable objects, living beings, scenery, and actions
            that appear in the image."""
            CAPTION = "caption"
            """Generate a human-readable caption sentence that describes the content of the image."""
            DENSE_CAPTIONS = "denseCaptions"
            """Generate human-readable caption sentences for up to 10 different regions in the image,
            including one for the whole image."""
            OBJECTS = "objects"
            """Object detection. This is similar to tags, but focused on detecting physical objects in the
            image and returning their location."""
            READ = "read"
            """Extract printed or handwritten text from the image. Also known as Optical Character Recognition
            (OCR)."""
            SMART_CROPS = "smartCrops"
            """Find representative sub-regions of the image for thumbnail generation, at desired aspect
            ratios, with priority given to detected faces."""
            PEOPLE = "people"
            """Detect people in the image and return their location."""
        ```


    - Langchain Azure AI Service Image Analysis Tool: [libs/community/langchain_community/tools/azure_ai_services/image_analysis.py](https://github.com/langchain-ai/langchain/blob/master/libs/community/langchain_community/tools/azure_ai_services/image_analysis.py#L70-L75)

        ``` python
        class AzureAiServicesImageAnalysisTool(BaseTool):

            """Tool that queries the Azure AI Services Image Analysis API.

            In order to set this up, follow instructions at:
            https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library-40
            """

            ... some code ...

                values["visual_features"] = [
                    VisualFeatures.TAGS,
                    VisualFeatures.OBJECTS,
                    VisualFeatures.CAPTION,
                    VisualFeatures.READ,
                ]

                return values

        ```
    
    Other references:  
    - [Quickstart: Image Analysis 4.0](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library-40?tabs=visual-studio%2Cwindows&pivots=programming-language-python)
    - [What is Image Analysis?](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview-image-analysis?tabs=4-0)











# Azure AI Custom Vision

# LangChain's Azure AI Github Issues

## My Q&A
### ❓Azure AI Vision v.s. Azure AI Custom Vision
The key difference is Azure AI Vision uses pre-built models that are ready to use _v.s._ [Azure AI Custom Vision]() allows users to upload their own images and manually annotate them to train their own custom vision models.

### ❓Azure AI Services Toolkit v.s. Azure Cognitive Services Toolkit
Cognitive service is now under Azure AI Service.
[As of July 2023, Azure AI services encompass all of what were previously known as Cognitive Services and Azure Applied AI Services.](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview?view=doc-intel-4.0.0)

### ❓OpenAI's AzureOpenAI() v.s. langchain_openai's AzureOpenAI()












