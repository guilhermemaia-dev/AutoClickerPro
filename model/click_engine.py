import time
import threading
import sys

IS_WINDOWS = sys.platform.startswith("win")
if IS_WINDOWS:
    import ctypes
else:
    import pyautogui

class ClickEngine:
    def __init__(self):
        self.running = False
        self.button = "left"
        self.click_type = "single"
        self.interval = 0.1
        self._thread = None

    def start(self, interval_secs=0.1, button="left", click_type="single"):
        if not self.running:
            self.running = True
            self.interval = max(0, interval_secs)
            self.button = button.lower()
            self.click_type = click_type.lower()
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def stop(self):
        self.running = False

    def click(self):
        click_count = 2 if self.click_type == "double" else 1

        if IS_WINDOWS:
            events = {"right": (0x0008, 0x0010), "middle": (0x0020, 0x0040), "left": (0x0002, 0x0004)}

            down_event, up_event = events.get(self.button, events["left"])

            for _ in range(click_count):
                ctypes.windll.user32.mouse_event(down_event, 0, 0, 0, 0)
                ctypes.windll.user32.mouse_event(up_event, 0, 0, 0, 0)

                if click_count > 1:
                    time.sleep(0.01)

        else:
            pyautogui.click(button=self.button, clicks=click_count)


    def _loop(self):
        try:
            while self.running:
                self.click()

                if self.interval > 0.02:
                    time.sleep(self.interval)
                else:
                    time.sleep(0.02)

        except Exception:
            self.running = False