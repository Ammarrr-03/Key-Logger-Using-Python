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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

# Set up logging
logging.basicConfig(filename='keylogger_detection.log', level=logging.INFO, format='%(asctime)s: %(message)s')

# Global variables
key_sequence = ""
is_running = True
key_counts = []
timestamps = []

# Set to keep track of currently pressed keys
pressed_keys = set()

def on_press(key):
    global key_sequence, key_counts, timestamps
    try:
        # Use str(key) instead of key.char for consistent character logging
        if key not in pressed_keys:
            pressed_keys.add(key)
            # Append the character to the sequence
            key_sequence += str(key).replace("'", "")  # Replace to handle single quotes around character
            logging.info(f'Key pressed: {key} at {datetime.now()}')
            key_counts.append(len(key_sequence))
            timestamps.append(datetime.now().strftime('%H:%M:%S'))
    except AttributeError:
        if key not in pressed_keys:
            pressed_keys.add(key)
            logging.info(f'Special key pressed: {key} at {datetime.now()}')
            if key == pynput.keyboard.Key.space:
                key_sequence += " "
            elif key == pynput.keyboard.Key.enter:
                key_sequence += "\n"

def on_release(key):
    try:
        pressed_keys.remove(key)
    except KeyError:
        pass

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
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, 'wptw vdti myxp mlkp')
            server.sendmail(sender, recipient, msg.as_string())
        print("Email alert sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def show_desktop_notification(message):
    try:
        notification.notify(
            title="Keylogger Detection Alert",
            message=message,
            timeout=5
        )
        print("Desktop notification sent!")
    except Exception as e:
        print(f"Failed to send desktop notification: {e}")

def detect_keylogger():
    global key_sequence, is_running
    suspicious_patterns = [
        r'\bpassword\b',
        r'\bemail\b',
        r'\blogin\b',
        r'\busername\b',
        r'\bcredit card\b',
        r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
        r'\b(\+?\d{1,2}\s?)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}\b'
    ]

    while is_running:
        time.sleep(5)
        print(f"Key sequence so far: {key_sequence}")

        for pattern in suspicious_patterns:
            if re.search(pattern, key_sequence, re.IGNORECASE):
                print(f'Suspicious activity detected: {pattern}')
                send_email_alert(pattern)
                show_desktop_notification(f'Suspicious activity detected: {pattern}')
                key_sequence = ""  # Clear sequence after detection

def monitor_keyboard():
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def update_graph(i):
    if len(timestamps) > 0:
        plt.cla()
        plt.plot(timestamps, key_counts, label="Key Press Count")
        plt.xlabel('Time')
        plt.ylabel('Key Presses')
        plt.title('Real-Time Key Press Activity')
        plt.legend()

def start_detection_with_graph():
    global is_running
    is_running = True
    print("Starting detection with real-time graph...")

    detection_thread = threading.Thread(target=detect_keylogger)
    detection_thread.start()

    keyboard_thread = threading.Thread(target=monitor_keyboard)
    keyboard_thread.start()

    fig = plt.figure()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    ani = animation.FuncAnimation(fig, update_graph, interval=1000)
    canvas.draw()

def stop_detection():
    global is_running
    is_running = False
    print("Stopping detection...")

# GUI setup
root = tk.Tk()
root.title("Keylogger Detection")

start_button = tk.Button(root, text="Start Detection with Graph", command=start_detection_with_graph)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Detection", command=stop_detection)
stop_button.pack(pady=10)

def on_closing():
    stop_detection()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
