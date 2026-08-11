import pynput

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

        repeat_til_stopped = self.view.repeat_til_stopped.get()

        if repeat_til_stopped == "true":
            rep_times = 0
        else:
            rep_times = int(self.view.entry_repeat_times.get() or 0)


        mode = self.view.frame2.mode_select.get()
        action_type = self.view.frame2.action_type.get().lower()

        if mode == "Keyboard":
            key_to_press = self.view.frame2.selected_key

            if not key_to_press:
                self.view.show_warning("SELECT A KEY!")
                return

            if key_to_press == "f6":
                self.view.show_warning("F6 IS RESERVED!")
                return

            self.model.start_keyboard(interval, key_to_press, rep_times, is_random, random_start, random_end, action_type)
        else:
            selected_mouse_button = self.view.frame2.mouse_button_select.get()
            selected_click_type = self.view.frame2.click_type.get()
            self.model.start(interval, selected_mouse_button, selected_click_type, rep_times, is_random, random_start, random_end, action_type)

        self.view.update_status(True)
        self.check_still_running()

    def check_still_running(self):
        self.view.frame2.update_click_display(self.model.counter_clicks)

        if self.model.running:
            self.view.after(100, self.check_still_running)
        else:
            self.view.update_status(False)


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