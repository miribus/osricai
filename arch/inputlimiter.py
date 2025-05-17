prev_key = None  # Store previous key
import curses

def handle_input(stdscr):
    global prev_key
    key = stdscr.getch()
    strkey = str(stdscr.getch())
    print("key", key)
    print("strkey", strkey)

    if key == prev_key:
        return None  # Ignore repeated input while holding key
    print("prev_key", prev_key)
    prev_key = key  # Store current key press
    return key if key != -1 else None  # Return valid keypress or None

def reset_key():
    """Reset previous key when player releases input."""
    global prev_key
    prev_key = None  # Clear stored key