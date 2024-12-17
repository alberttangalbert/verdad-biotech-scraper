import time
import pandas as pd
import os 

from app import run_indication_classifier
from app.config import Config

def main():
    """
    Main function to run the indication classifier on company descriptions
    and save the results to a CSV file.
    """

    # Validate application configuration
    Config.validate()

    # File paths for input and output
    input_file_path = "data/raw/biotech_comp_descriptions.csv"
    output_file_path = "data/processed/biotech_comp_indication_areas.csv"

    # Load company description data
    description_data = pd.read_csv(input_file_path)
    company_ids = description_data.iloc[:, 0].tolist()[:1]
    company_descriptions = description_data.iloc[:, 1].tolist()[:1]

    # Run the indication classifier
    print("Running the indication classifier...")
    start_time = time.time()
    processed_df = run_indication_classifier(company_ids, company_descriptions)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Save the processed data to a CSV file
    processed_df.to_csv(output_file_path, index=False)
    print(f"Results saved to '{output_file_path}'")

if __name__ == "__main__":
    main()
