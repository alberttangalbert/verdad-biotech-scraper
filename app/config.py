import os

class Config:
    # Azure OpenAI Configuration
    AZURE_OPENAI_API_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-01-preview")
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

    @classmethod
    def validate(cls):
        """Ensures all required configuration values are set and raises an error if any are missing."""
        
        # Required configurations and descriptions
        required_configs = {
            "AZURE_OPENAI_API_ENDPOINT": "Azure OpenAI endpoint",
            "AZURE_OPENAI_API_KEY": "Azure OpenAI API key",
            "AZURE_OPENAI_API_VERSION": "Azure OpenAI API version",
            "AZURE_OPENAI_DEPLOYMENT_NAME": "Azure OpenAI deployment name"
        }

        # Check for missing configurations
        missing_configs = [name for name, description in required_configs.items() if not getattr(cls, name)]
        
        if missing_configs:
            raise EnvironmentError(
                f"The following environment variables are missing: {', '.join(missing_configs)}. "
                "Please check your environment variables and set them accordingly."
            )