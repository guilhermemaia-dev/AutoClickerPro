import customtkinter as ctk

class MainWindowFrame(ctk.CTkFrame):
    def __init__(self, master, window, **kwargs):
        super().__init__(master, **kwargs)
        self.window = window
        self.offsetx = 0
        self.offsety = 0

    def enable_drag_on(self, widget):
        widget.bind("<Button-1>", self._save_pos)
        widget.bind("<B1-Motion>", self._move)

    def _save_pos(self, event):
        self.offsetx = event.x
        self.offsety = event.y

    def _move(self, event):
        x = self.winfo_pointerx() - self.offsetx
        y = self.winfo_pointery() - self.offsety
        self.window.geometry(f"+{x}+{y}")