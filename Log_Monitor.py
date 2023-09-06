import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Specify the path to your log file
log_file_path = '/Users/PRINCESSSADIYA/Downloads/Log_Monitor_Project/Log_Monitor.py'

# Define the error pattern you want to monitor
error_pattern = r'ERROR: (.*)'  # Adjust this pattern to match your log format

# Define your email settings
smtp_server = 'smtp.gmail.com'  # SMTP server address
smtp_port = 587  # SMTP server port
smtp_username = 'saadhsyed1@gmail.com'  # Your email address
smtp_password = '9000788056Ms'  # Your email password
sender_email = 'saadhsyed1@gmail.com'  # Sender email address
recipient_email = 'syed.saadh143@gmail.com'  # Recipient email address

def send_email(subject, message, attachment=None):
    # Create a MIME message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach text message
    msg.attach(MIMEText(message, 'plain'))

    # Attach file (if specified)
    if attachment:
        with open(attachment, "rb") as f:
            attach = MIMEApplication(f.read(),_subtype="pdf")
        attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
        msg.attach(attach)

    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")

def monitor_log(log_file_path):
    if not os.path.exists(log_file_path):
        print(f"An error occurred while monitoring the log: Log file not found: {log_file_path}")
        return

    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            match = re.search(error_pattern, line)
            if match:
                error_message = match.group(1)
                print(f"Error detected in log: {error_message}")
                send_email("Error Detected in Log", f"Error Message: {error_message}")

if __name__ == "__main__":
    monitor_log(log_file_path)
