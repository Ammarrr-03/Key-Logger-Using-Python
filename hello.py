import pynput
import time
import logging

# Setup logging
logging.basicConfig(filename='keylogger_detection.log', level=logging.INFO, format='%(asctime)s: %(message)s')

# Function to log key press
def on_press(key):
    try:
        logging.info(f'Key pressed: {key.char}')
    except AttributeError:
        logging.info(f'Special key pressed: {key}')

# Function to monitor keyboard activity
def monitor_keyboard():
    with pynput.keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Function to check for keylogger behavior
def detect_keylogger():
    suspicious_patterns = ['password', 'secret', 'username', 'login']  # Example patterns to watch for
    start_time = time.time()
    threshold_time = 60  # Time period to check for patterns (in seconds)
    
    while True:
        time.sleep(1)  # Check every second
        current_time = time.time()
        if current_time - start_time > threshold_time:
            # Read log file and check for suspicious patterns
            with open('keylogger_detection.log', 'r') as log_file:
                logs = log_file.readlines()
                for pattern in suspicious_patterns:
                    if any(pattern in log for log in logs):
                        print(f'Suspicious activity detected: {pattern}')
                        return  # Stop detection on suspicious activity
            start_time = current_time  # Reset timer

if __name__ == "__main__":
    print("Monitoring keyboard activity...")
    monitor_keyboard()  # Start monitoring keyboard
    detect_keylogger()  # Start detecting keylogger behavior
