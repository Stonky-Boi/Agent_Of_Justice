import csv
import sys

csv.field_size_limit(sys.maxsize)

def load_case_data(filepath):
    """
    Loads summaries from a CSV file with one summary per line, no header.
    Returns a list of dicts: {'summary': ...}
    """
    cases = []
    with open(filepath, mode="r", encoding="utf-8") as file:
        for line in file:
            summary = line.strip()
            if summary:
                cases.append({"summary": summary})
    return cases
