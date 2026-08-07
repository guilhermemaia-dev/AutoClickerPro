import time
import pyautogui
import threading

class ClickEngine:
    def __init__(self):
        self.running = False
        self.interval = 0.1
        self._thread = None

    def start(self, interval_ms):
        if not self.running:
            self.running = True
            self.interval = max(0.01, interval_ms / 1000)
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def stop(self):
        self.running = False

    def _loop(self):
        while self.running:
            pyautogui.click()
            time.sleep(self.interval)