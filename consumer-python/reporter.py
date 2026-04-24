import json

def generate_report(differences, report_path):
    """
    Generates and saves the analysis report to a JSON file.
    """
    with open(report_path, 'w') as f:
        json.dump(differences, f, indent=4, default=str)  # default=str for datetime