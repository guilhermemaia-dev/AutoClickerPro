import customtkinter as ctk
import config
from view.components.theme import Colors

class SettingsView(ctk.CTkFrame):
    def __init__(self, master_container, master_view):
        super().__init__(master_container, width=163, height=311, fg_color=Colors.BG_MAIN, bg_color="transparent", corner_radius=12, border_width=1, border_color=Colors.BOX_HOVER)

        self.master_container = master_container
        self.master_view = master_view
        self.master_view.is_settings_open = True

        self.configs = config.load_settings()

        self.current_hotkey = self.configs.get("hotkey", "F6").upper()

        self.pack_propagate(False)
        self.build_interface()
        self.build_safe_info_frame()

        if self.configs.get("border", True): self.switch_border.select()
        if self.configs.get("clicks", True): self.switch_clicks_count.select()
        if self.configs.get("dark_theme"): self.switch_dark_theme.select()
        if self.configs.get("topmost", True): self.switch_topMost.select()
        if self.configs.get("safety_lock", True): self.switch_safety_lock.select()

        self.btn_choose_hotkey.configure(text=self.current_hotkey)


    def build_interface(self):
        title_bar = ctk.CTkFrame(self, fg_color="transparent", height=35)
        title_bar.pack(fill="x", padx=10, pady=(8, 0))

        lbl_title = ctk.CTkLabel(title_bar, text="Settings", font=("Arial", 13, "bold"), text_color=Colors.TEXT_TITLE)
        lbl_title.pack(side="left", padx=10)

        btn_close = ctk.CTkButton(title_bar, text="✕", width=28, height=28, corner_radius=14, fg_color=Colors.BTN_HOVER, hover_color=Colors.WARNING_BG, text_color=Colors.TEXT_NORMAL, command=self.close_window)
        btn_close.pack(side="right")

        self.master_container.enable_drag_on(title_bar)
        self.master_container.enable_drag_on(lbl_title)

        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)


        # BORDER
        lbl_disable_border = ctk.CTkLabel(content_frame, text="Border", text_color=Colors.TEXT_NORMAL)
        lbl_disable_border.grid(row=0, column=0, padx=(0,4), pady=8, sticky="w")

        self.switch_border = ctk.CTkSwitch(content_frame, text="", command=self.save_and_update, width=40, progress_color=Colors.SWITCH_BTN)
        self.switch_border.grid(row=0, column=1, padx=4, pady=8, sticky="e")


        #CLICKS COUNT
        lbl_disable_clicks_count = ctk.CTkLabel(content_frame, text="Clicks", text_color=Colors.TEXT_NORMAL)
        lbl_disable_clicks_count.grid(row=1, column=0, padx=(0,4), pady=8, sticky="w")

        self.switch_clicks_count = ctk.CTkSwitch(content_frame, text="", command=self.save_and_update, width=40, progress_color=Colors.SWITCH_BTN)
        self.switch_clicks_count.grid(row=1, column=1, padx=4, pady=8, sticky="e")


        #DARK/LIGHT THEME
        lbl_dark_theme = ctk.CTkLabel(content_frame, text="Dark Theme", text_color=Colors.TEXT_NORMAL)
        lbl_dark_theme.grid(row=2, column=0, padx=(0,4), pady=8, sticky="w")

        self.switch_dark_theme = ctk.CTkSwitch(content_frame, text="", command=self.save_and_update, width=40, progress_color=Colors.SWITCH_BTN)
        self.switch_dark_theme.grid(row=2, column=1, padx=4, pady=8, sticky="e")


        # TOPMOST
        lbl_topMost = ctk.CTkLabel(content_frame, text="TopMost", text_color=Colors.TEXT_NORMAL)
        lbl_topMost.grid(row=3, column=0, padx=(0,4), pady=8, sticky="w")

        self.switch_topMost = ctk.CTkSwitch(content_frame, text="", command=self.save_and_update, width=40, progress_color=Colors.SWITCH_BTN)
        self.switch_topMost.grid(row=3, column=1, padx=4, pady=8, sticky="e")


        # SAFETY LOCK
        frame_safety = ctk.CTkFrame(content_frame, fg_color="transparent")
        frame_safety.grid(row=4, column=0, padx=(0,4), pady=8, sticky="w")

        lbl_safety_lock = ctk.CTkLabel(frame_safety, text="Safe Mode", text_color=Colors.TEXT_NORMAL)
        lbl_safety_lock.pack(side="left")

        btn_safe_info = ctk.CTkButton(frame_safety, text="?", width=18, height=18, corner_radius=9, fg_color=Colors.BOX_COLOR, hover_color=Colors.BOX_HOVER, text_color=Colors.TEXT_NORMAL, font=("Arial", 11, "bold"), command=self.show_safety_info)
        btn_safe_info.pack(side="left", padx=(5,0))

        self.switch_safety_lock = ctk.CTkSwitch(content_frame, text="", command=self.save_and_update, width=40, progress_color=Colors.SWITCH_BTN)
        self.switch_safety_lock.grid(row=4, column=1, padx=4, pady=8, sticky="e")


        # HOTKEY BUTTON
        lbl_choose_hotkey_btn = ctk.CTkLabel(content_frame, text="Hotkey", text_color=Colors.TEXT_NORMAL)
        lbl_choose_hotkey_btn.grid(row=5, column=0, padx=4, pady=8, sticky="w")

        self.btn_choose_hotkey = ctk.CTkButton(content_frame, text="Select Key", width=20, corner_radius=10, fg_color=Colors.BOX_COLOR, hover_color=Colors.BOX_HOVER, text_color=Colors.TEXT_NORMAL, command=self.start_listening_key)
        self.btn_choose_hotkey.place(relx=0.36, rely=0.895)



    # METHOD TO BUILD THE SAFETY LOCK FRAME

    def build_safe_info_frame(self):
        self.info_frame = ctk.CTkFrame(self, fg_color=Colors.BG_MAIN, corner_radius=10, border_width=2, border_color=Colors.WARNING_BG)

        lbl_warn_title = ctk.CTkLabel(self.info_frame, text="WARNING!", font=("Arial", 12, "bold"), text_color=Colors.WARNING_BG)
        lbl_warn_title.pack(pady=(10, 2))

        lbl_msg = ctk.CTkLabel(self.info_frame, text="If disabled, the AutoClicker can reach extremely high CPS.\n\nThis may cause lag!\nNot recommended.", font=("Arial", 12), text_color=Colors.TEXT_NORMAL, justify="center", wraplength=140)
        lbl_msg.pack(padx=8, pady=5)

        btn_ok = ctk.CTkButton(self.info_frame, text="Got it", width=70, height=24, fg_color=Colors.BOX_COLOR, hover_color=Colors.BOX_HOVER, text_color=Colors.TEXT_NORMAL, command=self.hide_safety_info)
        btn_ok.pack(pady=(5, 10))

    def show_safety_info(self):
        self.info_frame.place(relx=0.5, rely=0.44, anchor="center", relwidth=0.92)
        self.info_frame.lift()

    def hide_safety_info(self):
        self.info_frame.place_forget()


    #METHOD TO SAVE THE CURRENT CONFIGS

    def save_and_update(self):
        new_configs = {"border": bool(self.switch_border.get()), "clicks": bool(self.switch_clicks_count.get()), "dark_theme": bool(self.switch_dark_theme.get()), "topmost": bool(self.switch_topMost.get()), "safety_lock": bool(self.switch_safety_lock.get()), "hotkey": self.current_hotkey}
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
        self.btn_choose_hotkey.configure(text="Press...", fg_color=Colors.BTN_ACTIVE_KEY)
        self.btn_choose_hotkey.focus_set()
        top_window = self.winfo_toplevel()
        top_window.bind("<Key>", self.on_key_captured)

    def on_key_captured(self, event):
        top_window = self.winfo_toplevel()
        top_window.unbind("<Key>")
        
        self.current_hotkey = event.keysym.upper()
        self.btn_choose_hotkey.configure(text=self.current_hotkey, fg_color=Colors.BOX_COLOR)

        self.save_and_update()