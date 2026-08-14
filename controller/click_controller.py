import pynput
import time
import config
from view.components.theme import Colors

class ClickController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.btn_start.configure(command=self.start_clicking)
        self.view.btn_stop.configure(command=self.stop_clicking)

        self.reload_configs()

        self.shortcut = pynput.keyboard.Listener(on_press=self._on_key_press)
        self.shortcut.start()

        self.view.frame2.btn_get_coords.configure(command=self.start_getting_coords)

    def on_mouse_move(self, x, y):
        self.view.after(0, self.view.update_tooltip_pos, x, y)

    def on_mouse_click(self, x, y, button, pressed):
        if pressed and button == pynput.mouse.Button.left:
            self.view.after(0, self.view.hide_tooltip)
            self.view.after(0, self.update_coords_ui, int(x), int(y))
            return False

    def start_getting_coords(self):
        if hasattr(self, 'mouse_listener') and self.mouse_listener.is_alive():
            self.mouse_listener.stop()
            
        self.view.show_tooltip()
        self.view.btn_get_coords.configure(text="Click...", fg_color=Colors.BTN_ACTIVE_KEY)
        self.mouse_listener = pynput.mouse.Listener(on_move=self.on_mouse_move, on_click=self.on_mouse_click)
        self.mouse_listener.start()


    def update_coords_ui(self, x, y):
        self.view.entry_coords_x.delete(0, 'end')
        self.view.entry_coords_x.insert(0, str(x))
        self.view.entry_coords_y.delete(0, 'end')
        self.view.entry_coords_y.insert(0, str(y))

        self.view.location_mode.set("specific")
        self.view.btn_get_coords.configure(text="Get", fg_color=Colors.BOX_COLOR)

    def total_seconds(self):
        try:
            h = float(self.view.entry_hour.get() or 0)
            m = float(self.view.entry_mins.get() or 0)
            s = float(self.view.entry_secs.get() or 0)
            ms = float(self.view.entry_millis.get() or 0)

            total_seconds = (h*3600) + (m*60) + s + (ms/1000)

            return total_seconds
        
        except ValueError:
            self.view.show_warning("ONLY NUMBERS!")
            return None

    def start_clicking(self):
        if self.view.is_settings_open:
            return
        
        self.view.unbind("<Key>")

        is_fixed = self.view.click_option.get()
        is_random = False
        interval = 0.1
        random_start = 0.1
        random_end = 0.2

        self.initial_timer_str = self.view.frame2.entry_timer.get()

        if is_fixed == "false":
            is_random = True
            start = int(self.view.entry_random_millis_start.get() or 100)
            end = int(self.view.entry_random_millis_end.get() or 200)
            random_start = start / 1000
            random_end = end / 1000
        else:
            is_random = False
            interval = self.total_seconds()
            if interval is None:
                return

        repeat_mode = self.view.repeat_mode.get()
        rep_times = 0
        duration = 0

        if repeat_mode == "times":
            rep_times = int(self.view.entry_repeat_times.get() or 0)
        elif repeat_mode == "timer":
            duration = self.view.frame2.get_timer_secs()
            if duration <= 0:
                self.view.show_warning("TIMER MUST BE > 0!")
                return

        mode = self.view.frame2.mode_select.get()
        action_type = self.view.frame2.action_type.get().lower()
        location_mode = self.view.location_mode.get()

        target_x = None
        target_y = None
        if location_mode == "specific" and mode != "Keyboard":
            try:
                target_x = int(self.view.entry_coords_x.get())
                target_y = int(self.view.entry_coords_y.get())
            except ValueError:
                self.view.show_warning("INVALID X OR Y!")
                return

        if mode == "Keyboard":
            key_to_press = self.view.frame2.selected_key

            if not key_to_press:
                self.view.show_warning("SELECT A VALID KEY!")
                return

            if key_to_press.upper() == self.hotkey:
                self.view.show_warning(f"{self.hotkey} IS RESERVED!")
                return

            selected_click_type = self.view.frame2.click_type.get()
            self.model.start_keyboard(interval, key_to_press, selected_click_type, rep_times, duration, is_random, random_start, random_end, action_type)
        else:
            selected_mouse_button = self.view.frame2.mouse_button_select.get()
            selected_click_type = self.view.frame2.click_type.get()

            self.model.start(interval, selected_mouse_button, selected_click_type, rep_times, duration, is_random, random_start, random_end, action_type, target_x, target_y)

        self.view.update_status(True)
        self.check_still_running()

    def check_still_running(self):
        self.view.frame2.update_click_display(self.model.counter_clicks)

        if self.model.running:
            if self.view.repeat_mode.get() == "timer":
                elapsed = time.time() - self.model.start_time
                remaining_secs = max(0, int(self.model.duration - elapsed))
                self.view.frame2.update_timer_display(remaining_secs)

            self.view.after(100, self.check_still_running)
        else:
            self.view.update_status(False)
            if self.view.repeat_mode.get() == "timer":
                self.view.frame2.entry_timer.delete(0, "end")
                self.view.frame2.entry_timer.insert(0, self.initial_timer_str)


    def stop_clicking(self):
        self.model.stop()
        self.view.update_status(False)

    def toggle(self):
        if self.model.running:
            self.stop_clicking()
        else:
            self.start_clicking()

    def _on_key_press(self, key):
        key_name = str(key).replace("'","").replace("Key.", "").upper()

        if key_name == self.hotkey:
            self.view.after(0, self.toggle)

    def reload_configs(self):
        current_configs = config.load_settings()
        self.hotkey = current_configs.get("hotkey", "F6").upper()

        self.view.btn_start.configure(text=f"Start ({self.hotkey})")
        self.view.btn_stop.configure(text=f"Stop ({self.hotkey})")

        show_border = current_configs.get("border", True)
        self.view.apply_border(show_border)

        show_clicks = current_configs.get("clicks", True)
        self.view.frame2.apply_clicks(show_clicks)

        is_dark = current_configs.get("dark_theme", True)
        self.view.apply_theme(is_dark)

        is_topmost = current_configs.get("topmost", True)
        self.view.apply_topmost(is_topmost)

        is_safe = current_configs.get("safety_lock", True)
        self.model.safety_lock = is_safe