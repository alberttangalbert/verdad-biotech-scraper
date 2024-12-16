import ast
from typing import List
from app.services.azure.azure_openai_service import AzureOpenaiService

def create_system_prompt(indication_areas: List[str]) -> str:
    """
    Creates the system prompt string given a list of indication areas.
    The prompt instructs the model to return a Python list of strings
    representing indication areas.
    """
    return (
        "You are an expert in biotech domains. "
        "Given the description of a biotech company below, identify the indication areas that the company is focused on. "
        f"Possible indication areas are: {', '.join(indication_areas)}. "
        "Return your answer strictly as a Python list of strings (e.g., [\"Oncology\", \"Neurology\"]). "
        "Do not include any explanation or text outside the list. "
        "If you are unsure or no indication areas match, return an empty list (e.g., [])."
    )

def parse_indication_areas(response: str) -> List[str]:
    """
    Parses the chatbot's response into a list of indication areas.
    The response should be a Python list in string form, e.g. ["Oncology", "Neurology"].
    Returns an empty list if parsing fails or the format is invalid.
    """
    try:
        data = ast.literal_eval(response)
        if isinstance(data, list) and all(isinstance(item, str) for item in data):
            return data
    except (SyntaxError, ValueError):
        pass
    return []

def get_indication_areas_from_description(
    description: str, 
    azure_service: AzureOpenaiService, 
    system_prompt: str, 
    max_retries: int = 3
) -> List[str]:
    """
    Given a company description, queries the Azure OpenAI service to find the indication areas.
    Tries up to 'max_retries' times if parsing fails or the response is invalid.
    Returns a list of indication areas or an empty list if unsuccessful.

    :param description: The company's description text.
    :param azure_service: An initialized instance of AzureOpenaiService.
    :param system_prompt: The system prompt that guides the model's output format.
    :param max_retries: Maximum number of attempts before returning an empty list.
    :return: A list of indication areas as strings.
    """
    user_prompt = f"Company description:\n{description}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    for _ in range(max_retries):
        response = azure_service.query(messages=messages)
        areas = parse_indication_areas(response)
        if areas is not None:
            return areas

    # If all retries fail, return an empty list
    return []
