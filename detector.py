import time
import ctypes
import threading
import json
import os
import mss
import cv2
import numpy as np
import keyboard

# Low-level Windows API constants for raw hardware mouse events
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

def win32_click(x, y):
    """
    Direct Windows API mouse input simulation to bypass game engine / Vanguard input filtering.
    """
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    
    # Convert pixel coords to absolute normalized coordinates (0 to 65535)
    normalized_x = int(x * 65535 / screen_width)
    normalized_y = int(y * 65535 / screen_height)
    
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.01)
    
    # Event down and up
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.02)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

class InstalockDetector:
    def __init__(self, config_path="config.json", status_callback=None):
        self.config_path = config_path
        self.status_callback = status_callback
        self.running = False
        self.selected_agent = "Jett"
        self.lock_thread = None
        self.sct = mss.mss()
        self.load_config()

        # Bind F8 global abort hotkey
        keyboard.add_hotkey("f8", self.abort_search)

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "lock_in_button": {"x": 960, "y": 815},
                "agents": {"Jett": {"x": 704, "y": 925}},
                "detection": {"scan_delay_ms": 10, "lock_delay_sec": 0.05}
            }

    def set_agent(self, agent_name):
        self.selected_agent = agent_name

    def update_status(self, state, message=""):
        if self.status_callback:
            self.status_callback(state, message)

    def abort_search(self):
        if self.running:
            self.running = False
            self.update_status("IDLE", "Aborted via F8")

    def start_instalock(self):
        if self.running:
            return
        self.running = True
        self.update_status("SEARCHING", f"Searching for {self.selected_agent}...")
        self.lock_thread = threading.Thread(target=self._instalock_loop, daemon=True)
        self.lock_thread.start()

    def stop_instalock(self):
        self.running = False
        self.update_status("IDLE", "Stopped")

    def _instalock_loop(self):
        agent_coords = self.config.get("agents", {}).get(self.selected_agent)
        lock_coords = self.config.get("lock_in_button", {"x": 960, "y": 815})
        scan_delay = self.config.get("detection", {}).get("scan_delay_ms", 10) / 1000.0
        lock_delay = self.config.get("detection", {}).get("lock_delay_sec", 0.05)

        if not agent_coords:
            self.running = False
            self.update_status("IDLE", f"Coordinates missing for {self.selected_agent}")
            return

        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

        while self.running:
            # Grab frame fast using mss (<5ms)
            sct_img = self.sct.grab(monitor)
            frame = np.array(sct_img)

            # Rapid dual-click sequence: Agent Icon -> Lock In Button
            try:
                # Click agent coordinates
                win32_click(agent_coords["x"], agent_coords["y"])
                time.sleep(lock_delay)
                
                # Click Lock In button coordinates
                win32_click(lock_coords["x"], lock_coords["y"])
                time.sleep(lock_delay)
                
                # Check if successful lock sequence finished
                self.running = False
                self.update_status("LOCKED", f"LOCKED {self.selected_agent.upper()}!")
                break
            except Exception as e:
                time.sleep(scan_delay)

        if not self.running and self.status_callback:
            pass
