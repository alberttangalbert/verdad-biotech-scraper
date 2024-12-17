# verdad-biotech-scraper

## Description
The biotech scraper takes in descriptions of companies and uses a LLM to extract specific information.
The output is a binary classification table, where each row corresponds to a company and columns represent the presence (1) or absence (0) of various indication areas.+++++

## Methodology 
The scraper uses the Azure Openai GPT models to perform categorization. 
(example output: `[Oncology, Respiratory, Gastrointestinal/Hepatology]`)
The system prompting enforces structured outpput from the GPT model. 
Then a parser compiles the string response into a Python list, 
retrying on failure and returning an empty list if parsing fails.

## Environment Set-up 
1. Copy the `.env.example` file to `.env` in the root of the project:
   ```
   $ cp .env.example .env
   ```
2. Populate the `.env` file
3. Create environment 
   ```
   $ python -m venv venv
   ```
4. Activate the virtual environment
    > Linux/macOS
    ```
   $ source venv/bin/activate
   ```
   > Windows Git Bash 
   ```
   $ source venv/Scripts/activate
   ```
5. Install requirements
    ```
   $ pip install -r requirements.txt
   ```
6. Add .env variables to environment
    ```
    export $(cat .env)
    ```

## Retrive Data 
1. Log into the `PSA31288.us-east-1` Snowflake account
2. Navigate to `Projects` and create new SQL Worksheet
3. Select `Intern` for `Role` and `COMPUTE_WH` for `Run on Warehouse`
4. Select `BIOTECH_PROJECT` for `Databases` and `READ_ONLY` for `Schemas`
5. Run this SQL command to fetch descriptions from "DESCRIPTIONS" table
    ```
    SELECT COMPANY_ID, IQ_BUSINESS_DESCRIPTION
    FROM DESCRIPTIONS;
    ```
6. Download the results as a .csv file
7. Rename the .csv file to "biotech_comp_addresses.csv"
8. Place the .csv file in the "data/raw" folder as "biotech_comp_descriptions.csv"
    ```
    data/raw/biotech_comp_addresses.csv
    ```

## To-run  
```
python run.py
```

## Output 
Indication areas classification .csv file 
```
data/processed/biotech_comp_indication_areas.csv
```
| company_id | Oncology | Neurology | Cardiovascular | ... | Respiratory | Urology | ... |
|------------|----------|-----------|----------------|-----|-------------|---------|-----|
| 25240322   | 1        | 1         | 0              | ... | 1           | 0       | ... |
| 213080     | 1        | 0         | 0              | ... | 0           | 0       | ... |
| 36018      | 1        | 0         | 1              | ... | 1           | 0       | ... |
| 262431     | 0        | 0         | 0              | ... | 0           | 1       | ... |
| 625814292  | 0        | 1         | 1              | ... | 0           | 0       | ... |
| 4493417    | 0        | 0         | 0              | ... | 0           | 0       | ... |


## To-do (if approved)
Run classification on indications/disease areas by prevalence
- Rare diseases
- Pediatrics
- Acute
- Chronic

Run classification on indications/disease areas by modality
- Proteins
    - Mono clone antibody
    - Others 
- Peptides
    - Amino acids greater than 40
    - AA less than 40
    - Cyclic peptide
- Small molecules
- RNA
    - siRNA, ASO, etc
- CGT therapy
- Vaccines

Run classification on indications/disease areas by target types
- GPCR
- Kinase
- Ion channel
- Nuclear receptors
- Others

Other areas to consider 
- Clinical stage, regulatory path, innovations, team, IP
