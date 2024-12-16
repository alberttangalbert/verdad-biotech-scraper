from dotenv import load_dotenv

from app.services.azure.azure_openai_service import AzureOpenaiService
from app.config import Config

load_dotenv()
Config.validate()

# Initialize the Azure OpenAI service
azure_openai_service = AzureOpenaiService()
print(azure_openai_service.query("What is the capital of France?"))