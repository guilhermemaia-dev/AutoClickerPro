import customtkinter as ctk
from view.components.main_window_frame import MainWindowFrame
from view.frames.frame1 import Frame1
from view.frames.frame2 import Frame2
from view.frames.frame3 import Frame3

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainView(ctk.CTk):
    def __init__(self, controller=None):
        super().__init__()

        self.controller = controller

        self.overrideredirect(True)
        self.geometry("500x400")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color="#171427")
        self.click_option = ctk.StringVar(value="true")

        self.main_container = MainWindowFrame(self, window=self, corner_radius=0, border_width=1.5, border_color="#ff4757", fg_color="#171427")
        self.main_container.pack(fill="both", expand=True)

        self.build_header()

        self.frame1 = Frame1(self.main_container, click_option_var=self.click_option)
        self.frame1.pack(side="top", fill="x", padx=15, pady=8)

        self.frame2 = Frame2(self.main_container)
        self.frame2.pack(side="top", fill="x", padx=15, pady=8)

        self.frame3 = Frame3(self.main_container)
        self.frame3.pack(side="top", fill="x", padx=15, pady=8)

        self.btn_start = self.frame3.btn_start
        self.btn_stop = self.frame3.btn_stop
        
        self.lbl_status = self.frame2.lbl_status

        self.entry_hour = self.frame1.entry_hour
        self.entry_mins = self.frame1.entry_mins
        self.entry_secs = self.frame1.entry_secs
        self.entry_millis = self.frame1.entry_millis
        self.entry_random_millis_start = self.frame1.entry_random_millis_start
        self.entry_random_millis_end = self.frame1.entry_random_millis_end



    def build_header(self):
        title_bar = ctk.CTkFrame(self.main_container, fg_color="transparent", height=35)
        title_bar.pack(fill="x", padx=10, pady=(8, 0))

        lbl_title = ctk.CTkLabel(title_bar, text="Auto Clicker PRO", font=("Arial", 13, "bold"), text_color="#b1a6c7")
        lbl_title.pack(side="left", padx=10)

        self.main_container.enable_drag_on(title_bar)
        self.main_container.enable_drag_on(lbl_title)

        window_controls = ctk.CTkFrame(title_bar, fg_color="transparent")
        window_controls.pack(side="right")

        btn_minimize = ctk.CTkButton(window_controls, text="─", width=28, height=28, corner_radius=14,fg_color="#27243F", hover_color="#3b3759", command=self.minimize_window)
        btn_minimize.pack(side="left", padx=(0, 6))

        btn_close = ctk.CTkButton(window_controls, text="✕", width=28, height=28, corner_radius=14, fg_color="#27243F", hover_color="#ff4757", command=self.destroy)
        btn_close.pack(side="left")


    def minimize_window(self):
        self.overrideredirect(False)
        self.iconify()
        self.bind("<FocusIn>", self.on_deiconify)

    def on_deiconify(self, event=None):
        if self.state() == "normal":
            self.overrideredirect(True)
            self.unbind("<FocusIn>")

    def animated_status(self):
        if not self.running_state:
            return

        animated_lst = ["RUNNING.", "RUNNING..", "RUNNING..."]

        if self.status_index % 2 == 0:
            laser_color = "#00ff9f"
        else:
            laser_color = "#00b8ff"

        self.main_container.configure(border_color=laser_color)
        self.lbl_status.configure(text=animated_lst[self.status_index], text_color="#00ff9f")
        self.status_index = (self.status_index + 1) % len(animated_lst)
        self.after(400, self.animated_status)

    def update_status(self, running):
        self.running_state = running

        if running:
            self.status_index = 0
            self.main_container.configure(border_color="#00ff9f", border_width=1.5)
            self.btn_start.configure(state="disabled")
            self.animated_status()
        else:
            self.lbl_status.configure(text="Status: STOPPED", text_color="red")
            self.main_container.configure(border_color="#ff0055", border_width=1.5)
            self.btn_start.configure(state="normal")

