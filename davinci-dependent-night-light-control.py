import sys
import time
import threading
import logging
import os
import ctypes
from logging.handlers import RotatingFileHandler

import psutil
import keyboard
import pystray
from PIL import Image, ImageDraw
from nightlight import NightLight  # <-- Imports from your local nightlight.py

# --- Single-instance guard (Windows named mutex) ---
_MUTEX_NAME = "Global\\DaVinciNightLightControl_SingleInstance"
_mutex = ctypes.windll.kernel32.CreateMutexW(None, False, _MUTEX_NAME)
if ctypes.windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
    ctypes.windll.user32.MessageBoxW(
        None,
        "DaVinci Night Light Control is already running.",
        "Already Running",
        0x30,  # MB_ICONWARNING
    )
    sys.exit(1)

# --- Configuration ---
PROCESS_NAME = "Resolve.exe"  # DaVinci Resolve's executable name
HOTKEY = "ctrl+alt+n"         # Shortcut to toggle night light
CHECK_INTERVAL = 3            # Seconds between checks

# --- Logging Setup ---
# When frozen by PyInstaller, __file__ points to the temp _MEIPASS dir.
# sys.executable always points to the actual .exe (or .py when running normally).
_base_dir = (
    os.path.dirname(sys.executable)
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)
_log_path = os.path.join(_base_dir, "davinci-night-light.log")
_handler = RotatingFileHandler(
    _log_path,
    maxBytes=2 * 1024 * 1024,  # 2 MB per file
    backupCount=3,              # Keep up to 3 rotated files
    encoding="utf-8",
)
_handler.setFormatter(logging.Formatter(
    fmt="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
))

log = logging.getLogger("NightLightAuto")
log.setLevel(logging.DEBUG)
log.addHandler(_handler)
# Also mirror to the console so existing print-style debugging still works
log.addHandler(logging.StreamHandler())

# --- State variables ---
app_enabled = True
davinci_was_running = False

# Initialize the NightLight class from the repo
nl = NightLight()


def set_nightlight(enable_mode: bool):
    """
    Controls Windows Night Light using the local nightlight.py script.
    enable_mode: True (turn on) or False (turn off)
    """
    action = "ON" if enable_mode else "OFF"
    try:
        if enable_mode:
            nl.enable()
        else:
            nl.disable()
        log.info("Night light turned %s.", action)
    except Exception as e:
        log.error("Failed to turn night light %s: %s", action, e, exc_info=True)


def monitor_davinci():
    global davinci_was_running

    log.info("Monitor thread started. Watching for '%s' every %ds.", PROCESS_NAME, CHECK_INTERVAL)

    # Default to ON when the app first boots
    set_nightlight(True)

    while True:
        try:
            if app_enabled:
                # Check if DaVinci Resolve is running
                is_running = any(
                    proc.name() == PROCESS_NAME
                    for proc in psutil.process_iter(["name"])
                )

                if is_running and not davinci_was_running:
                    # DaVinci just opened -> Turn Night Light OFF
                    log.info("DaVinci Resolve detected — disabling night light.")
                    set_nightlight(False)
                    davinci_was_running = True

                elif not is_running and davinci_was_running:
                    # DaVinci just closed -> Turn Night Light ON
                    log.info("DaVinci Resolve closed — re-enabling night light.")
                    set_nightlight(True)
                    davinci_was_running = False
            else:
                log.debug("App is disabled; skipping process check.")
        except Exception as e:
            log.error("Unexpected error in monitor loop: %s", e, exc_info=True)

        time.sleep(CHECK_INTERVAL)


# --- Interactions ---
def on_hotkey():
    if app_enabled:
        try:
            nl.toggle()
            log.info("Hotkey (%s) triggered — night light toggled.", HOTKEY)
        except Exception as e:
            log.error("Hotkey toggle failed: %s", e, exc_info=True)
    else:
        log.warning("Hotkey pressed but app is currently disabled; ignoring.")


def on_reload(icon, item):
    global davinci_was_running
    log.info("Reload requested via tray — resetting davinci_was_running state.")
    davinci_was_running = False


def on_toggle_app(icon, item):
    global app_enabled
    app_enabled = not app_enabled
    log.info("App monitoring %s via tray toggle.", "ENABLED" if app_enabled else "DISABLED")


def on_exit(icon, item):
    log.info("Exit requested via tray — shutting down.")
    icon.stop()


def create_tray_icon():
    image = Image.new("RGB", (64, 64), color=(30, 30, 40))
    dc = ImageDraw.Draw(image)
    dc.ellipse([16, 16, 48, 48], fill=(250, 200, 50))
    return image


def main():
    log.info("=== DaVinci-Dependent Night Light Control starting ===")
    log.info("Log file: %s", _log_path)

    # 1. Register global shortcut
    keyboard.add_hotkey(HOTKEY, on_hotkey)
    log.info("Registered hotkey: %s", HOTKEY)

    # 2. Start monitoring thread
    monitor_thread = threading.Thread(target=monitor_davinci, daemon=True)
    monitor_thread.start()

    # 3. System Tray icon
    menu = pystray.Menu(
        pystray.MenuItem("Reload", on_reload),
        pystray.MenuItem("Enabled", on_toggle_app, checked=lambda item: app_enabled),
        pystray.MenuItem("Exit", on_exit),
    )

    icon = pystray.Icon("NightLightAuto", create_tray_icon(), "Night Light Auto-Manager", menu)
    log.info("Tray icon running.")
    icon.run()
    log.info("=== DaVinci-Dependent Night Light Control stopped ===")


if __name__ == "__main__":
    main()