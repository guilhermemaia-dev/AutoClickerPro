import pynput

class ClickController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.btn_start.configure(command=self.start_clicking)
        self.view.btn_stop.configure(command=self.stop_clicking)

        self.shortcut = pynput.keyboard.Listener(on_press=self._on_key_press)
        self.shortcut.start()


    def start_clicking(self):
        interval = max(0.01, 500 / 1000)
        self.model.start(interval)
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