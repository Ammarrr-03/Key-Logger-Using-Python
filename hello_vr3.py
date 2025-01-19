import pynput
import time
import logging
import smtplib
from email.mime.text import MIMEText
from plyer import notification
import re
from datetime import datetime
import tkinter as tk
import threading

# Setup logging
logging.basicConfig(filename='keylogger_detection.log', level=logging.INFO, format='%(asctime)s: %(message)s')

# Variable to collect all key presses
key_sequence = ""
is_running = True  # To control the monitoring thread

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

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(sender, 'your_password')
            server.sendmail(sender, recipient, msg.as_string())
        print("Email alert sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to show desktop notification
def show_desktop_notification(message):
    try:
        notification.notify(
            title="Keylogger Detection Alert",
            message=message,
            timeout=5  # seconds
        )
        print("Desktop notification sent!")
    except Exception as e:
        print(f"Failed to send desktop notification: {e}")

# Function to monitor and detect suspicious patterns using regex
def detect_keylogger():
    global key_sequence, is_running
    suspicious_patterns = [
        r'\bpassword\b',      # Detects the word "password"
        r'\bemail\b',         # Detects the word "email"
        r'\blogin\b',         # Detects the word "login"
        r'\busername\b',      # Detects the word "username"
        r'\bcredit card\b',   # Detects the phrase "credit card"
        r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'  # Detects credit card numbers
    ]

    while is_running:
        time.sleep(5)  # Check every 5 seconds
        print(f"Key sequence so far: {key_sequence}")  # Debugging statement

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

# Start detection in a separate thread
def start_detection():
    global is_running
    is_running = True
    print("Starting detection...")
    detection_thread = threading.Thread(target=detect_keylogger)
    detection_thread.start()

    # Start keyboard monitoring in a separate thread
    keyboard_thread = threading.Thread(target=monitor_keyboard)
    keyboard_thread.start()

def stop_detection():
    global is_running
    is_running = False
    print("Stopping detection...")

# GUI Setup using tkinter
root = tk.Tk()
root.title("Keylogger Detection")

start_button = tk.Button(root, text="Start Detection", command=start_detection)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Detection", command=stop_detection)
stop_button.pack(pady=10)

root.mainloop()
