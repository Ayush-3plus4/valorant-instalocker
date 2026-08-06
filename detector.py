import time
import json
import os
import threading
import mss
import cv2
import numpy as np
import pydirectinput
import keyboard

# Configure pydirectinput failsafe and pause settings
pydirectinput.FAILSAFE = False
pydirectinput.PAUSE = 0.01

class InstalockDetector:
    def __init__(self, config_path="config.json", status_callback=None):
        self.config_path = config_path
        self.status_callback = status_callback
        self.running = False
        self.selected_agent = "Jett"
        self.lock_thread = None
        self.sct = mss.mss()
        self.load_config()

        # Register global F8 abort hotkey
        try:
            keyboard.add_hotkey("f8", self.abort_search)
        except Exception:
            pass

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "resolution": "1920x1080",
                "lock_in_button": {"x": 960, "y": 815},
                "agents": {"Jett": {"x": 704, "y": 925}},
                "detection": {"scan_delay_ms": 10, "lock_delay_sec": 0.05, "match_threshold": 0.8}
            }

    def set_agent(self, agent_name):
        self.selected_agent = agent_name

    def update_status(self, state, message=""):
        if self.status_callback:
            self.status_callback(state, message)

    def abort_search(self):
        if self.running:
            self.running = False
            self.update_status("IDLE", "Aborted via F8 hotkey")

    def start_instalock(self):
        if self.running:
            return
        self.running = True
        self.update_status("SEARCHING", f"Scanning for {self.selected_agent}...")
        self.lock_thread = threading.Thread(target=self._instalock_loop, daemon=True)
        self.lock_thread.start()

    def stop_instalock(self):
        self.running = False
        self.update_status("IDLE", "Stopped")

    def match_template(self, screen_img, template_img, threshold=0.8):
        """
        Perform OpenCV template matching on captured screen frame.
        """
        if template_img is None or screen_img is None:
            return False, (0, 0)
        
        res = cv2.matchTemplate(screen_img, template_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        if max_val >= threshold:
            h, w = template_img.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return True, (center_x, center_y)
        return False, (0, 0)

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

        # Optional template matching file verification
        template_path = f"templates/{self.selected_agent.lower()}.png"
        template_img = cv2.imread(template_path) if os.path.exists(template_path) else None

        while self.running:
            # 1. Ultra-fast screen capture via mss
            sct_img = self.sct.grab(monitor)
            frame = cv2.cvtColor(np.array(sct_img), cv2.COLOR_BGRA2BGR)

            # 2. Template matching or coordinate fallback
            target_x, target_y = agent_coords["x"], agent_coords["y"]
            if template_img is not None:
                found, matched_coords = self.match_template(
                    frame, template_img, 
                    threshold=self.config.get("detection", {}).get("match_threshold", 0.8)
                )
                if found:
                    target_x, target_y = matched_coords

            # 3. High-speed DirectInput automation
            try:
                # Click target agent icon
                pydirectinput.moveTo(target_x, target_y)
                pydirectinput.click(target_x, target_y)
                time.sleep(lock_delay)

                # Click Lock In button
                pydirectinput.moveTo(lock_coords["x"], lock_coords["y"])
                pydirectinput.click(lock_coords["x"], lock_coords["y"])
                time.sleep(lock_delay)

                self.running = False
                self.update_status("LOCKED", f"LOCKED {self.selected_agent.upper()}!")
                break
            except Exception as e:
                time.sleep(scan_delay)
