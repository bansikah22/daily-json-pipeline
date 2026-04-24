import os
import json
import shutil
import logging
from analyzer import analyze_data

# Define absolute paths
BASE_DIR = "/app/shared-data"
INCOMING_DIR = os.path.join(BASE_DIR, "incoming")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
FAILED_DIR = os.path.join(BASE_DIR, "failed")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])

def main():
    logging.info("Starting consumer...")
    for dir_path in [INCOMING_DIR, PROCESSED_DIR, FAILED_DIR, REPORTS_DIR]:
        os.makedirs(dir_path, exist_ok=True)

    files_to_process = sorted([f for f in os.listdir(INCOMING_DIR) if f.endswith('.json')], reverse=True)
    
    if not files_to_process:
        logging.info("No new files to process.")
        return

    latest_file_path = os.path.join(INCOMING_DIR, files_to_process[0])
    previous_file_path = os.path.join(INCOMING_DIR, files_to_process[1]) if len(files_to_process) > 1 else None

    try:
        logging.info(f"Analyzing {latest_file_path}" + (f" and comparing with {previous_file_path}" if previous_file_path else ""))
        analysis = analyze_data(latest_file_path, previous_file_path)

        report_filename = os.path.basename(latest_file_path).replace(".json", "_report.json")
        report_path = os.path.join(REPORTS_DIR, report_filename)
        with open(report_path, "w") as f:
            json.dump(analysis, f, indent=4)
        logging.info(f"Analysis report saved to {report_path}")

        # Move all processed files
        for filename in files_to_process:
            shutil.move(os.path.join(INCOMING_DIR, filename), os.path.join(PROCESSED_DIR, filename))
        logging.info(f"Moved {len(files_to_process)} files to {PROCESSED_DIR}")

    except Exception as e:
        logging.error(f"Error processing files: {e}")
        # Move all incoming files to failed
        for filename in files_to_process:
            shutil.move(os.path.join(INCOMING_DIR, filename), os.path.join(FAILED_DIR, filename))
        logging.info(f"Moved {len(files_to_process)} files to {FAILED_DIR}")
            
    logging.info("Consumer finished.")

if __name__ == "__main__":
    main()
