import requests
import csv
import os

# Define the URL to fetch the data from the dataset
url = "https://datasets-server.huggingface.co/rows?dataset=jellyChiru%2FSParC&config=default&split=train"

# Fetch the JSON data from the URL
response = requests.get(url)
data = response.json()

# Path to the database directory containing metadata folders
database_dir = "database"

# Prepare the output CSV file
output_csv = "formatted_sparc.csv"

# Open the CSV file and write headers
with open(output_csv, mode="w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["text"])  # Header for single "text" column

    # Iterate through each row in the JSON data
    for row_data in data["rows"]:
        database_id = row_data["row"]["database_id"]
        question = row_data["row"]["question"]
        query = row_data["row"]["query"]
        
        # Path to the schema.sql file for the current database_id
        schema_file_path = os.path.join(database_dir, database_id, "schema.sql")

        # Extract metadata from schema.sql file
        if os.path.exists(schema_file_path):
            with open(schema_file_path, "r") as schema_file:
                metadata = schema_file.read()
        else:
            # print(f"Warning: Schema file for {database_id} not found.")
            metadata = ""

        # Construct the text entry
        text_entry = f"<s>[INST] {metadata} \n\n {question} [INST] {query} <s>"

        # Write the entry to the CSV file
        writer.writerow([text_entry])

print(f"Dataset saved to {output_csv}")
