import pynput
import time

class ClickController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.btn_start.configure(command=self.start_clicking)
        self.view.btn_stop.configure(command=self.stop_clicking)

        self.shortcut = pynput.keyboard.Listener(on_press=self._on_key_press)
        self.shortcut.start()


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

        if mode == "Keyboard":
            key_to_press = self.view.frame2.selected_key

            if not key_to_press:
                self.view.show_warning("SELECT A VALID KEY!")
                return

            if key_to_press == "f6":
                self.view.show_warning("F6 IS RESERVED!")
                return

            selected_click_type = self.view.frame2.click_type.get()
            self.model.start_keyboard(interval, key_to_press, selected_click_type, rep_times, duration, is_random, random_start, random_end, action_type)
        else:
            selected_mouse_button = self.view.frame2.mouse_button_select.get()
            selected_click_type = self.view.frame2.click_type.get()

            self.model.start(interval, selected_mouse_button, selected_click_type, rep_times, duration, is_random, random_start, random_end, action_type)

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
        if key == pynput.keyboard.Key.f6:
            self.view.after(0, self.toggle)