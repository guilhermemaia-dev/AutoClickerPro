import customtkinter as ctk

class Frame3(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#191729", corner_radius=12, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.btn_start = ctk.CTkButton(self, text="Start (F6)", font=("Arial", 13, "bold"), width=220, height=60)
        self.btn_start.grid(row=0, column=0, padx=5, pady=8)

        self.btn_stop = ctk.CTkButton(self, text="Stop (F6)", font=("Arial", 13, "bold"), width=220, height=60, state="disabled", fg_color="#B33535")
        self.btn_stop.grid(row=0, column=1, padx=5, pady=8)