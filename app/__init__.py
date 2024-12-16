import os
import pandas as pd

from app.services.azure.azure_openai_service import AzureOpenaiService
from app.core.indication_classifier import (
    create_system_prompt,
    get_indication_areas_from_description,
)

def run_indication_classifier(company_ids: list, company_descriptions: list) -> pd.DataFrame:
    """
    Runs the indication classifier to determine the focus areas of biotech companies.

    This function processes a list of company descriptions, uses the Azure OpenAI service to classify
    indication areas, and returns the results as a DataFrame where each row corresponds to a company.

    The output DataFrame contains:
        - 'company_id': The unique identifier for each company.
        - Columns for each possible indication area with binary values (1 if the company works in that area, 0 otherwise).

    :param company_ids: A list of unique company identifiers.
    :param company_descriptions: A list of descriptions corresponding to the companies.
    :return: A pandas DataFrame with indication areas classified for each company.
    :raises FileNotFoundError: If the `indication_areas.txt` file is not found.
    """
    # Path to the indication areas configuration file
    indication_areas_file = "data/config/indication_areas.txt"

    # Ensure the indication areas file exists
    if not os.path.exists(indication_areas_file):
        raise FileNotFoundError(f"The file '{indication_areas_file}' was not found.")

    # Load indication areas from the configuration file
    with open(indication_areas_file, "r") as file:
        indication_areas = [line.strip() for line in file if line.strip()]

    # Create the system prompt for the Azure OpenAI service
    system_prompt = create_system_prompt(indication_areas)

    # Initialize the Azure OpenAI service
    azure_openai_service = AzureOpenaiService()

    # List to store results for each company
    results = []

    # Process each company description and classify indication areas
    for company_id, description in zip(company_ids, company_descriptions):
        classified_areas = get_indication_areas_from_description(
            description, azure_openai_service, system_prompt
        )
        results.append({"company_id": company_id, "indication_areas": classified_areas})

    # Prepare the data for the output DataFrame
    processed_data = []
    for result in results:
        row = {"company_id": result["company_id"]}
        for area in indication_areas:
            row[area] = 1 if area in result["indication_areas"] else 0
        processed_data.append(row)

    # Convert the processed data into a pandas DataFrame
    return pd.DataFrame(processed_data)
