from datasets import load_dataset
import csv
import os
import glob

# Load the dataset
dataset = load_dataset("jellyChiru/SParC")

# Path to the database directory containing metadata folders
database_dir = "database"

# Prepare the output CSV file
output_csv = "formatted_sparc.csv"

# Open the CSV file and write headers
with open(output_csv, mode="w", newline="", encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["text"])  # Header for single "text" column

    # Process the 'train' split of the dataset
    for row in dataset['train']:
        database_id = row["database_id"]
        question = row["question"]
        query = row["query"]
        
        # Search for any .sql file in the current database_id folder
        sql_files = glob.glob(os.path.join(database_dir, database_id, "*.sql"))
        
        # Use the first .sql file found as the metadata source
        metadata = ""
        if sql_files:
            try:
                with open(sql_files[0], "r", encoding='utf-8') as sql_file:
                    # Read lines, excluding those starting with 'INSERT'
                    metadata = ''.join(line for line in sql_file if not (line.strip().upper().startswith("INSERT") or line.strip().upper().startswith("--")))
            except UnicodeDecodeError:
                print(f"Warning: Could not decode file {sql_files[0]}. Trying a different encoding.")
                with open(sql_files[0], "r", encoding='latin-1') as sql_file:
                    metadata = ''.join(line for line in sql_file if not (line.strip().upper().startswith("INSERT") or line.strip().upper().startswith("--")))
        else:
            print(f"Warning: No .sql file found for {database_id}.")
            metadata = ""

        # Construct the text entry
        text_entry = f"<s>[INST] {metadata} \n\n {question} [INST] {query} <s>"

        # Write the entry to the CSV file
        writer.writerow([text_entry])

print(f"Dataset saved to {output_csv}")
