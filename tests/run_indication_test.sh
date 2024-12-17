#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Setting up environment for testing..."

# Step 1: Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "Virtual environment created."
fi

# Step 2: Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    # Linux/macOS
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    # Windows (Git Bash, Command Prompt)
    source venv/Scripts/activate
else
    echo "Error: Could not find virtual environment activation script."
    exit 1
fi
echo "Virtual environment activated."

# Step 3: Install dependencies
pip install -r requirements.txt || echo "No requirements.txt found. Skipping..."

# Step 4: Load environment variables from .env
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
    echo "Environment variables loaded from .env"
else
    echo ".env file not found. Skipping environment variable setup."
fi

# Step 5: Run the indication classifier test
echo "Running the indication classifier..."
python -c "
import pandas as pd
from app import run_indication_classifier

# Load test data
test_data = pd.read_csv('tests/example_description_data.csv')

# Run the function
results = run_indication_classifier(
    company_ids=test_data['COMPANY_ID'].tolist(),
    company_descriptions=test_data['IQ_BUSINESS_DESCRIPTION'].tolist()
)

# Display results
print('Indication Areas Classification Results:')
print(results)
"
echo "Tests completed successfully!"