from openai import AzureOpenAI
from openai.types.chat import ChatCompletion

from app.config import Config

class AzureOpenaiService:
    def __init__(self):
        """
        Initializes the AzureOpenaiService instance.
        :param deployment_name: Optional deployment name. If not provided, it defaults to Config.AZURE_OPENAI_DEPLOYMENT.
        """

        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            api_key=Config.AZURE_OPENAI_API_KEY,
            api_version=Config.AZURE_OPENAI_API_VERSION,
            azure_endpoint=Config.AZURE_OPENAI_API_ENDPOINT,
        )
        self.deployment_name = Config.AZURE_OPENAI_DEPLOYMENT_NAME

    def query(self, prompt: str, temperature: float = 0.7):
        """
        Sends a user prompt to Azure OpenAI and retrieves the response.

        :param prompt: The input prompt to the OpenAI model.
        :param temperature: The temperature for the model's response (higher = more creative).
        :return: The content of the assistant's response.
        """
        try:
            # Make the API request
            response: ChatCompletion = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
            )

            # Return the assistant's response
            return response.choices[0].message.content.strip()

        except Exception as e:
            # Add helpful information to exceptions
            return f"Error querying Azure OpenAI: {str(e)}"