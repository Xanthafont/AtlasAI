import json
import os
from datetime import datetime

try:
    from colorama import init, Fore, Back, Style
    init()  # Initialize colorama
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

def safe_json_load(filepath, default=None):
    """Safely load JSON data from a file"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load {filepath}: {e}")
    
    return default if default is not None else {}

def safe_json_save(data, filepath):
    """Safely save JSON data to a file"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving to {filepath}: {e}")
        return False

def get_timestamp():
    """Get current timestamp in ISO format"""
    return datetime.now().isoformat()

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text, color="white", bold=False):
    """Print colored text to terminal"""
    if not COLORAMA_AVAILABLE:
        print(text)
        return
    
    color_map = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE
    }
    
    color_code = color_map.get(color.lower(), Fore.WHITE)
    style_code = Style.BRIGHT if bold else Style.NORMAL
    
    print(f"{style_code}{color_code}{text}{Style.RESET_ALL}")