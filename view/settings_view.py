import customtkinter as ctk
import config

class SettingsView(ctk.CTkFrame):
    def __init__(self, master_container, master_view, getters_box_color):
        super().__init__(master_container, width=163, height=311, fg_color="#171427", bg_color="transparent", corner_radius=12, border_width=1, border_color="#2b2648")

        self.getters_box_color = getters_box_color
        self.master_container = master_container
        self.master_view = master_view
        self.master_view.is_settings_open = True

        self.configs = config.load_settings()

        self.current_hotkey = self.configs.get("hotkey", "F6").upper()

        self.pack_propagate(False)
        self.build_interface()

        if self.configs["border"]: self.switch_border.select()
        if self.configs["clicks"]: self.switch_clicks_count.select()
        if self.configs["dark_theme"]: self.switch_dark_theme.select()

        self.btn_choose_hotkey.configure(text=self.current_hotkey)


    def build_interface(self):
        title_bar = ctk.CTkFrame(self, fg_color="transparent", height=35)
        title_bar.pack(fill="x", padx=10, pady=(8, 0))

        lbl_title = ctk.CTkLabel(title_bar, text="Settings", font=("Arial", 13, "bold"), text_color="#b1a6c7")
        lbl_title.pack(side="left", padx=10)

        btn_close = ctk.CTkButton(title_bar, text="✕", width=28, height=28, corner_radius=14, fg_color="#27243F", hover_color="#ff4757", command=self.close_window)
        btn_close.pack(side="right")

        self.master_container.enable_drag_on(title_bar)
        self.master_container.enable_drag_on(lbl_title)

        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        lbl_disable_border = ctk.CTkLabel(content_frame, text="Border")
        lbl_disable_border.grid(row=0, column=0, padx=(0,4), pady=8, sticky="w")

        self.switch_border = ctk.CTkSwitch(content_frame, text="", command=self.save_and_update)
        self.switch_border.grid(row=0, column=1, padx=4, pady=8, sticky="e")

        lbl_disable_clicks_count = ctk.CTkLabel(content_frame, text="Clicks")
        lbl_disable_clicks_count.grid(row=1, column=0, padx=(0,4), pady=8, sticky="w")

        self.switch_clicks_count = ctk.CTkSwitch(content_frame, text="", command=self.save_and_update)
        self.switch_clicks_count.grid(row=1, column=1, padx=4, pady=8, sticky="e")
        
        lbl_dark_theme = ctk.CTkLabel(content_frame, text="Dark Theme")
        lbl_dark_theme.grid(row=2, column=0, padx=(0,4), pady=8, sticky="w")

        self.switch_dark_theme = ctk.CTkSwitch(content_frame, text="", command=self.save_and_update)
        self.switch_dark_theme.grid(row=2, column=1, padx=4, pady=8, sticky="e")


        lbl_choose_hotkey_btn = ctk.CTkLabel(content_frame, text="Hotkey")
        lbl_choose_hotkey_btn.grid(row=3, column=0, padx=4, pady=8, sticky="w")

        self.btn_choose_hotkey = ctk.CTkButton(content_frame, text="Select Key", width=20, corner_radius=10, fg_color=self.getters_box_color, hover_color="#2b2640", command=self.start_listening_key)
        self.btn_choose_hotkey.place(relx=0.36, rely=0.55)


    def save_and_update(self):
        new_configs = {"border": bool(self.switch_border.get()), "clicks": bool(self.switch_clicks_count.get()), "dark_theme": bool(self.switch_dark_theme.get()), "hotkey": self.current_hotkey}
        config.save_settings(new_configs)

        controller = getattr(self.master_view, "controller", None)
        if controller is not None:
            controller.reload_configs()

    def close_window(self):
        self.winfo_toplevel().unbind("<Key>")
        self.save_and_update()

        self.master_view.btn_start.configure(state="normal")
        self.master_view.is_settings_open = False
        self.destroy()

    def start_listening_key(self):
        self.btn_choose_hotkey.configure(text="Press...")
        self.btn_choose_hotkey.focus_set()
        top_window = self.winfo_toplevel()
        top_window.bind("<Key>", self.on_key_captured)


    def on_key_captured(self, event):
        top_window = self.winfo_toplevel()
        top_window.unbind("<Key>")
        
        self.current_hotkey = event.keysym.upper()
        self.btn_choose_hotkey.configure(text=self.current_hotkey)

        self.save_and_update()