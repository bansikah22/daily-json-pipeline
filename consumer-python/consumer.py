import os
import json
from analyzer import analyze_data
from reporter import generate_report

# Define paths
PROCESSED_DIR = "../shared-data/processed"

import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler("consumer.log"),
                              logging.StreamHandler()])

def main():
    logging.info("Starting consumer...")
    json_files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.json') and not f.startswith('report')]
    if not json_files:
        logging.info("No JSON files to process.")
        return

    # Sort by date, assume filename has date
    json_files.sort(reverse=True)  # Latest first

    # For simplicity, compare the latest two files
    if len(json_files) >= 2:
        latest = os.path.join(PROCESSED_DIR, json_files[0])
        previous = os.path.join(PROCESSED_DIR, json_files[1])
        differences = analyze_data(latest, previous)
    else:
        differences = analyze_data(os.path.join(PROCESSED_DIR, json_files[0]), None)

    # Generate report
    report_path = os.path.join(PROCESSED_DIR, f"report-{json_files[0].replace('.json', '')}.json")
    generate_report(differences, report_path)
    logging.info(f"Report generated: {report_path}")

if __name__ == "__main__":
    main()