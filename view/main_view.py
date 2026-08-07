import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Auto Click PRO")
        self.geometry("500x400")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        self.lbl_status = ctk.CTkLabel(self, text="Status: STOP", font=("Arial", 16, "bold"), text_color="red")
        self.lbl_status.pack(pady=(15,5))

        self.btn_start = ctk.CTkButton(self, text="START (F6)", font=("Arial", 16, "bold"))
        self.btn_start.pack(pady=5)

        self.btn_stop = ctk.CTkButton(self, text="STOP (F6)", font=("Arial", 16, "bold"))
        self.btn_stop.pack(pady=5)

    def update_status(self, running):
        if running:
            self.lbl_status.configure(text="Status: RUNNING", text_color="green")
        else:
            self.lbl_status.configure(text="Status: STOP", text_color="red")
