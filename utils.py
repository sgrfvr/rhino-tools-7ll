import csv
import os

def ensure_directory_exists(directory):
    """Ensure that the specified directory exists. If not, create it."""
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def write_csv(data, filename, folder='exports'):
    """Write the provided data to a CSV file in the specified folder.
    
    Args:
        data (list of dict): The data to write to the CSV, where each dict is a row.
        filename (str): The name of the CSV file to create.
        folder (str): The folder where the CSV will be saved.
    
    Raises:
        ValueError: If data is empty or not a list of dictionaries.
        IOError: If there is an issue writing to the file.
    """
    if not data or not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        raise ValueError("Data must be a non-empty list of dictionaries.")

    ensure_directory_exists(folder)
    
    file_path = os.path.join(folder, filename)
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    except IOError as e:
        print(f"Error writing to file {file_path}: {e}")
        raise

# TODO: Add functionality to append to existing CSV files
# TODO: Implement more flexible CSV formatting options (e.g., delimiter, quoting)
# TODO: Add unit tests for utility functions
# TODO: Consider handling different data types in the CSV export (e.g., lists, nested dicts)
