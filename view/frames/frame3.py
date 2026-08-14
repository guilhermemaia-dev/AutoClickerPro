import customtkinter as ctk
from view.components.theme import Colors

class Frame3(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Colors.BG_FRAME, corner_radius=12, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #START BUTTON
        self.btn_start = ctk.CTkButton(self, text="Start (F6)", font=("Arial", 13, "bold"), width=220, height=60, fg_color=Colors.BTN_START_BG, text_color=Colors.BTN_START_TEXT)
        self.btn_start.grid(row=0, column=0, padx=5, pady=8)

        #STOP BUTTON
        self.btn_stop = ctk.CTkButton(self, text="Stop (F6)", font=("Arial", 13, "bold"), width=220, height=60, state="disabled", fg_color=Colors.BTN_STOP_BG, text_color=Colors.BTN_STOP_TEXT)
        self.btn_stop.grid(row=0, column=1, padx=5, pady=8)