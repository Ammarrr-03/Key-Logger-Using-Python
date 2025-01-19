import pynput
import time
import logging
import smtplib
from email.mime.text import MIMEText
from plyer import notification
import re
from datetime import datetime
import tkinter as tk

# Setup logging
logging.basicConfig(filename='keylogger_detection.log', level=logging.INFO, format='%(asctime)s: %(message)s')

# Function to log key press with timestamp
def on_press(key):
    try:
        logging.info(f'Key pressed: {key.char} at {datetime.now()}')
    except AttributeError:
        logging.info(f'Special key pressed: {key} at {datetime.now()}')

# Function to send email alert
def send_email_alert(suspicious_activity):
    sender = 'ammararsiwala068@gmail.com'
    recipient = 'madman.0333333@gmail.com'
    subject = 'Suspicious Activity Detected'
    body = f'Suspicious activity detected: {suspicious_activity}'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(sender, 'your_password')
        server.sendmail(sender, recipient, msg.as_string())

# Function to show desktop notification
def show_desktop_notification(message):
    notification.notify(
        title="Keylogger Detection Alert",
        message=message,
        timeout=5  # seconds
    )

# Function to monitor and detect suspicious patterns using regex
def detect_keylogger():
    suspicious_patterns = [
        r'\bpassword\b', r'\bemail\b', r'\blogin\b', r'\busername\b', 
        r'\bcredit card\b', r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'  # Credit card regex
    ]
    start_time = time.time()
    threshold_time = 60  # Time period to check for patterns (in seconds)

    while True:
        time.sleep(1)
        current_time = time.time()
        if current_time - start_time > threshold_time:
            # Read log file and check for suspicious patterns
            with open('keylogger_detection.log', 'r') as log_file:
                logs = log_file.readlines()
                for pattern in suspicious_patterns:
                    for log in logs:
                        if re.search(pattern, log):
                            print(f'Suspicious activity detected: {pattern}')
                            send_email_alert(pattern)
                            show_desktop_notification(f'Suspicious activity detected: {pattern}')
                            return  # Stop detection on suspicious activity
            start_time = current_time  # Reset timer

# Function to monitor keyboard activity
def monitor_keyboard():
    with pynput.keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# GUI for starting/stopping detection
def start_detection():
    print("Starting detection...")
    monitor_keyboard()
    detect_keylogger()

def stop_detection():
    print("Stopping detection...")
    root.quit()

# GUI Setup using tkinter
root = tk.Tk()
root.title("Keylogger Detection")

start_button = tk.Button(root, text="Start Detection", command=start_detection)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Detection", command=stop_detection)
stop_button.pack(pady=10)

root.mainloop()
