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
        is_fixed = self.view.click_option.get()
        interval = self.total_seconds()

        if is_fixed == "false":
            from random import randint

            start = int(self.view.entry_random_millis_start.get() or 100)
            end = int(self.view.entry_random_millis_end.get() or 200)
            interval = randint(start, end)
            interval = float(interval / 1000)

        if interval is None:
            return

        selected_mouse_button = self.view.mouse_button_select.get()
        selected_click_type = self.view.click_type.get()
    
        self.model.start(interval, selected_mouse_button, selected_click_type)
        self.view.update_status(True)



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