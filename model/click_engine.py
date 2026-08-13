import time
import threading
import sys
import random
import pyautogui

IS_WINDOWS = sys.platform.startswith("win")
if IS_WINDOWS:
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

class ClickEngine:
    def __init__(self):
        self.running = False
        self.mode = "mouse"
        self.action_type = "click"
        self.button = "left"
        self.click_type = "single"
        self.key_to_press = None

        self.is_random = False
        self.interval = 0.1
        self.random_start = 0.1
        self.random_end = 0.2

        self.counter_clicks = 0
        self.rep_times = 0
        self._thread = None

        self.target_x = None
        self.target_y = None

        self.KEY_MAP = {
            'a': 0x1E, 'b': 0x30, 'c': 0x2E, 'd': 0x20, 'e': 0x12, 'f': 0x21, 'g': 0x22,
            'h': 0x23, 'i': 0x17, 'j': 0x24, 'k': 0x25, 'l': 0x26, 'm': 0x32, 'n': 0x31,
            'o': 0x18, 'p': 0x19, 'q': 0x10, 'r': 0x13, 's': 0x1F, 't': 0x14, 'u': 0x16,
            'v': 0x2F, 'w': 0x11, 'x': 0x2D, 'y': 0x15, 'z': 0x2C, 'space': 0x39,
            'shift': 0x2A, 'ctrl': 0x1D, 'alt': 0x38, 'enter': 0x1C,
            'backspace': 0x0E, '1': 0x02, '2': 0x03, '3': 0x04, '4': 0x05, '5': 0x06,
            '6': 0x07, '7': 0x08, '8': 0x09, '9': 0x0A, '0': 0x0B}

    def start(self, interval_secs=0.1, button="left", click_type="single", rep_times=0, duration=0, is_random=False, random_start=0.1, random_end=0.2, action_type="click", target_x=None, target_y=None):
        if not self.running:
            self.mode = "mouse"
            self.action_type = action_type
            self.counter_clicks = 0
            self.duration = duration
            self.start_time = time.time()
            self.running = True

            self.is_random = is_random
            self.interval = max(0, interval_secs)
            self.random_start = random_start
            self.random_end = random_end

            self.button = button.lower()
            self.click_type = click_type.lower()
            self.rep_times = rep_times

            self.target_x = target_x
            self.target_y = target_y

            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def start_keyboard(self, interval_secs=0.1, key_to_press="space", click_type="single", rep_times=0, duration=0, is_random=False, random_start=0.1, random_end=0.2, action_type="click"):
        if not self.running:
            self.mode = "keyboard"
            self.action_type = action_type
            self.counter_clicks = 0
            self.duration = duration
            self.start_time = time.time()
            self.running = True

            self.is_random = is_random
            self.interval = max(0, interval_secs)
            self.random_start = random_start
            self.random_end = random_end

            self.key_to_press = str(key_to_press).lower()
            self.click_type = click_type.lower()
            self.rep_times = rep_times

            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def stop(self):
        self.running = False

        if self.action_type == "hold":
            self.release_all()

    def get_current_interval(self):
        if self.is_random:
            return random.uniform(self.random_start, self.random_end)
        return self.interval

    def send_key_event(self, key, is_down):
        if not IS_WINDOWS:
            if is_down:
                pyautogui.keyDown(key)
            else:
                pyautogui.keyUp(key)
            return
        
        key_map = self.KEY_MAP.get(key.lower())
        if key_map:
            flags = 0x0008 if is_down else (0x0008 | 0x0002)
            ctypes.windll.user32.keybd_event(0, key_map, flags, 0)
        else:
            if is_down:
                pyautogui.keyDown(key)
            else:
                pyautogui.keyUp(key)

    def release_all(self):
        if self.mode == "keyboard" and self.key_to_press:
            self.send_key_event(self.key_to_press, is_down=False)
        else:
            if IS_WINDOWS:
                events_up = {"right": 0x0010, "middle": 0x0040, "left": 0x0004}
                up_event = events_up.get(self.button, 0x0004)
                ctypes.windll.user32.mouse_event(up_event, 0, 0, 0, 0)
            else:
                pyautogui.mouseUp(button=self.button)

    def press_down(self):
        if self.mode == "keyboard":
            self.send_key_event(self.key_to_press, is_down=True)
        else:
            if self.target_x is not None and self.target_y is not None:
                if IS_WINDOWS:
                    ctypes.windll.user32.SetCursorPos(self.target_x, self.target_y)
                else:
                    pyautogui.moveTo(self.target_x, self.target_y)

            if IS_WINDOWS:
                events_down = {"right": 0x0008, "middle": 0x0020, "left": 0x0002}
                down_event = events_down.get(self.button, 0x0002)
                ctypes.windll.user32.mouse_event(down_event, 0, 0, 0, 0)
            else:
                pyautogui.mouseDown(button=self.button)


    def click_keyboard(self):
        press_count = 2 if self.click_type == "double" else 1

        for i in range(press_count):
            if IS_WINDOWS:
                self.send_key_event(self.key_to_press, is_down=True)
                time.sleep(0.02)
                self.send_key_event(self.key_to_press, is_down=False)
            else:
                pyautogui.press(self.key_to_press)

            if press_count > 1 and i == 0:
                time.sleep(0.08)

    def click_mouse(self):
        click_count = 2 if self.click_type == "double" else 1

        if self.target_x is not None and self.target_y is not None:
            if IS_WINDOWS:
                ctypes.windll.user32.SetCursorPos(self.target_x, self.target_y)
            else:
                pyautogui.click(x=self.target_x, y=self.target_y, button=self.button, clicks=click_count)
                return

        if IS_WINDOWS:
            events = {"right": (0x0008, 0x0010), "middle": (0x0020, 0x0040), "left": (0x0002, 0x0004)}
            down_event, up_event = events.get(self.button, events["left"])

            for i in range(click_count):
                ctypes.windll.user32.mouse_event(down_event, 0, 0, 0, 0)
                ctypes.windll.user32.mouse_event(up_event, 0, 0, 0, 0)

                if click_count > 1 and i == 0:
                    time.sleep(0.01)
        else:
            pyautogui.click(button=self.button, clicks=click_count)


    def _loop(self):
        try:
            if self.action_type == "hold":
                self.press_down()
                while self.running:
                    if self.duration > 0 and (time.time() - self.start_time) >= self.duration:
                        break
                    time.sleep(0.05)
                self.release_all()
                self.running = False
                return

            while self.running and (self.rep_times <= 0 or self.counter_clicks < self.rep_times):
                if self.duration > 0 and (time.time() - self.start_time) >= self.duration:
                    break

                if self.mode == "keyboard":
                    self.click_keyboard()
                else:
                    self.click_mouse()

                self.counter_clicks += 1

                sleep_time = self.get_current_interval()
                time.sleep(max(0.02, sleep_time))

        except Exception:
            pass
        finally:
            self.release_all()
            self.running = False