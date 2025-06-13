import json
from typing import Text


def load_json_file(file_path: Text):
    """
    Load JSON data from a file containing multiple JSON objects.

    :file_path: Path to the JSON file.

    :return: List of JSON objects as Python dictionaries.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = [json.loads(line) for line in file]

    return data
