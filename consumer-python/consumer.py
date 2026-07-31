import os
import json
import shutil
import logging
import smtplib
from email.mime.text import MIMEText
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

def send_email(subject, body):
    """Sends an email notification."""
    try:
        smtp_host = os.environ.get("SMTP_HOST")
        smtp_port = int(os.environ.get("SMTP_PORT", 587))
        smtp_user = os.environ.get("SMTP_USER")
        smtp_pass = os.environ.get("SMTP_PASS")
        mail_to = os.environ.get("MAIL_TO")
        mail_from = os.environ.get("MAIL_FROM")

        if not all([smtp_host, smtp_port, smtp_user, smtp_pass, mail_to, mail_from]):
            logging.warning("Email configuration is incomplete. Skipping email notification.")
            return

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = mail_from
        msg["To"] = mail_to

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(mail_from, [mail_to], msg.as_string())
            logging.info(f"Successfully sent email notification to {mail_to}")

    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def main():
    logging.info("Starting consumer...")
    status = "SUCCESS"
    message = "Data pipeline ran successfully."

    for dir_path in [INCOMING_DIR, PROCESSED_DIR, FAILED_DIR, REPORTS_DIR]:
        os.makedirs(dir_path, exist_ok=True)

    files_to_process = sorted([f for f in os.listdir(INCOMING_DIR) if f.endswith('.json')], reverse=True)
    
    if not files_to_process:
        logging.info("No new files to process.")
        send_email("Data Pipeline: No Data", "The data pipeline ran but found no new files to process.")
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

        message += f"\n\n- Processed {len(files_to_process)} file(s).\n- Report generated at {report_path}."

        # Move all processed files
        for filename in files_to_process:
            shutil.move(os.path.join(INCOMING_DIR, filename), os.path.join(PROCESSED_DIR, filename))
        logging.info(f"Moved {len(files_to_process)} files to {PROCESSED_DIR}")

    except Exception as e:
        status = "FAILURE"
        message = f"Data pipeline failed with an error: {e}"
        logging.error(message)
        # Move all incoming files to failed
        for filename in files_to_process:
            shutil.move(os.path.join(INCOMING_DIR, filename), os.path.join(FAILED_DIR, filename))
        logging.info(f"Moved {len(files_to_process)} files to {FAILED_DIR}")
            
    finally:
        subject = f"Data Pipeline: {status}"
        send_email(subject, message)
        logging.info("Consumer finished.")

if __name__ == "__main__":
    main()
