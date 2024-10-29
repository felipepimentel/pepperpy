# pypepper/utils/file_utils.py
import csv
import json


def read_json(file_path):
    """Read JSON data from a file."""
    with open(file_path, "r") as f:
        return json.load(f)


def write_json(data, file_path):
    """Write JSON data to a file."""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def read_csv(file_path):
    """Read CSV data from a file."""
    with open(file_path, newline="") as f:
        return list(csv.reader(f))


def write_csv(data, file_path):
    """Write data to a CSV file."""
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)
