import time
import threading
import psutil
import keyboard
import pystray
from PIL import Image, ImageDraw
from nightlight import NightLight  # <-- Imports from your local nightlight.py

# --- Configuration ---
PROCESS_NAME = "Resolve.exe"  # DaVinci Resolve's executable name
HOTKEY = "ctrl+alt+n"         # Shortcut to toggle night light
CHECK_INTERVAL = 3            # Seconds between checks

# State variables
app_enabled = True
davinci_was_running = False

# Initialize the NightLight class from the repo
nl = NightLight()

def set_nightlight(enable_mode):
    """
    Controls Windows Night Light using the local nightlight.py script.
    enable_mode: True (turn on) or False (turn off)
    """
    try:
        if enable_mode:
            nl.enable()
        else:
            nl.disable()
    except Exception as e:
        print(f"Error changing night light state: {e}")

def monitor_davinci():
    global davinci_was_running
    
    # Default to ON when the app first boots
    set_nightlight(True)
    
    while True:
        if app_enabled:
            # Check if DaVinci Resolve is running
            is_running = any(proc.name() == PROCESS_NAME for proc in psutil.process_iter(['name']))
            
            if is_running and not davinci_was_running:
                # DaVinci just opened -> Turn Night Light OFF
                set_nightlight(False)
                davinci_was_running = True
                
            elif not is_running and davinci_was_running:
                # DaVinci just closed -> Turn Night Light ON (Default)
                set_nightlight(True)
                davinci_was_running = False
                
        time.sleep(CHECK_INTERVAL)

# --- Interactions ---
def on_hotkey():
    if app_enabled:
        try:
            nl.toggle()
        except Exception:
            pass

def on_reload(icon, item):
    global davinci_was_running
    davinci_was_running = False 

def on_toggle_app(icon, item):
    global app_enabled
    app_enabled = not app_enabled

def on_exit(icon, item):
    icon.stop()

def create_tray_icon():
    image = Image.new('RGB', (64, 64), color=(30, 30, 40))
    dc = ImageDraw.Draw(image)
    dc.ellipse([16, 16, 48, 48], fill=(250, 200, 50))
    return image

def main():
    # 1. Register global shortcut
    keyboard.add_hotkey(HOTKEY, on_hotkey)

    # 2. Start monitoring thread
    monitor_thread = threading.Thread(target=monitor_davinci, daemon=True)
    monitor_thread.start()

    # 3. System Tray icon
    menu = pystray.Menu(
        pystray.MenuItem('Reload', on_reload),
        pystray.MenuItem('Enabled', on_toggle_app, checked=lambda item: app_enabled),
        pystray.MenuItem('Exit', on_exit)
    )
    
    icon = pystray.Icon("NightLightAuto", create_tray_icon(), "Night Light Auto-Manager", menu)
    icon.run()

if __name__ == "__main__":
    main()