import csv
import sys

csv.field_size_limit(sys.maxsize)

def load_case_data(filepath):
    """
    Loads case data from a CSV file.
    Returns a list of dictionaries, one per case.
    Each dictionary should have: summary, plaintiff, defendant, etc.
    """
    cases = []
    with open(filepath, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cases.append({
                "summary": row.get("summary", ""),
                "plaintiff": row.get("plaintiff", ""),
                "defendant": row.get("defendant", ""),
                "prosecution_arguments": row.get("prosecution_arguments", ""),
                "defense_arguments": row.get("defense_arguments", ""),
                "witnesses": row.get("witnesses", "")
            })
    return cases
