import customtkinter as ctk

class Frame3(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#191729", corner_radius=12, **kwargs)


        self.btn_start = ctk.CTkButton(self, text="START (F6)", font=("Arial", 16, "bold"), width=150, height=60)
        self.btn_start.grid(row=0, column=0)

        self.btn_stop = ctk.CTkButton(self, text="STOP (F6)", font=("Arial", 16, "bold"), width=150, height=60)
        self.btn_stop.grid(row=0, column=1)