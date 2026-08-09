import customtkinter as ctk

class Frame2(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#191729", corner_radius=12, height=80, **kwargs)

        self.lbl_status = ctk.CTkLabel(self, text="Status: STOPPED", font=("Arial", 16, "bold"), text_color="red")
        self.lbl_status.grid(row=0, column=2)