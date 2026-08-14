import customtkinter as ctk
import tkinter as tk
from view.components.main_window_frame import MainWindowFrame
from view.frames.frame1 import Frame1
from view.frames.frame2 import Frame2
from view.frames.frame3 import Frame3
from view.settings_view import SettingsView
from view.components.theme import Colors
import ctypes
import config
import os
import sys

# FUNCTION TO FIND FILES IN THE PYINSTALLER TEMPORARY FOLDER
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

saved_configs = config.load_settings()
theme = "Dark" if saved_configs.get("dark_theme", True) else "Light"
ctk.set_appearance_mode(theme)

class MainView(ctk.CTk):
    def __init__(self, controller=None):
        super().__init__()

        self.controller = controller

        self.overrideredirect(True)
        self.title("Auto Clicker Pro")
        self.geometry("500x400")
        self.resizable(False, False)
        is_topmost = saved_configs.get("topmost", True)
        self.attributes("-topmost", is_topmost)
        self.configure(fg_color="#000000")
        self.wm_attributes("-transparentcolor", "#000000")
        try:
            icon_file = resource_path("assets/autoclicker.ico")
            self.iconbitmap(icon_file)
        except Exception:
            pass

        self.click_option = ctk.StringVar(value="true")
        self.repeat_mode = ctk.StringVar(value="until_stopped")
        self.location_mode = ctk.StringVar(value="current")

        self.main_container = MainWindowFrame(self, window=self, corner_radius=12, border_width=1, border_color=Colors.BORDER_LASER_STOPPED, fg_color=Colors.BG_MAIN)
        self.main_container.pack(fill="both", expand=True)

        self.build_header()

        self.frame1 = Frame1(self.main_container, click_option_var=self.click_option)
        self.frame1.pack(side="top", fill="x", padx=15, pady=4)

        self.frame2 = Frame2(self.main_container, repeat_mode_var=self.repeat_mode, location_mode_var=self.location_mode)
        self.frame2.pack(side="top", fill="x", padx=15, pady=4)

        self.frame3 = Frame3(self.main_container)
        self.frame3.pack(side="top", fill="x", padx=15, pady=4)

        #SHORTCUTS

        self.btn_start = self.frame3.btn_start
        self.btn_stop = self.frame3.btn_stop

        self.mouse_button_select = self.frame2.mouse_button_select
        self.click_type = self.frame2.click_type
        self.entry_hour = self.frame1.entry_hour
        self.entry_mins = self.frame1.entry_mins
        self.entry_secs = self.frame1.entry_secs
        self.entry_millis = self.frame1.entry_millis
        self.entry_random_millis_start = self.frame1.entry_random_millis_start
        self.entry_random_millis_end = self.frame1.entry_random_millis_end
        self.entry_repeat_times = self.frame2.entry_repeat_times
        
        self.btn_get_coords = self.frame2.btn_get_coords
        self.entry_coords_x = self.frame2.entry_coords_x
        self.entry_coords_y = self.frame2.entry_coords_y

        self.tooltip = tk.Toplevel(self)
        self.tooltip.overrideredirect(True)
        self.tooltip.attributes("-topmost", True)
        self.tooltip.withdraw() 
        self.tooltip_label = tk.Label(self.tooltip, text="X: 0 Y: 0", bg="#333", fg="white", font=("Arial", 9))
        self.tooltip_label.pack(ipadx=4, ipady=2)

        self.bind_all("<Button-1>", self.clear_focus)

        self.after(10, self.set_taskbar_icon)

        self.is_settings_open = False

        
    #METHOD TO CLEAR FOCUS WHEN CLICKING OUTSIDE THE ENTRY

    def clear_focus(self, event):
        widget = event.widget

        if isinstance(widget, str):
            try:
                widget = self.nametowidget(widget)
            except Exception:
                return

        if hasattr(widget, "winfo_class"):
            widget_class = str(widget.winfo_class()).lower()
            if "entry" not in widget_class:
                self.focus()

    #MAIN METHOD FOR DISPLAYING THE WARNINGS

    def show_warning(self, message):
        warning = ctk.CTkFrame(self.main_container, fg_color=Colors.WARNING_BG, corner_radius=8)
        warning.place(relx=0.55, rely=0.055, anchor="center")

        warning.lift()

        lbl_warning = ctk.CTkLabel(warning, text=message, text_color=Colors.TEXT_TITLE, font=("Arial", 11, "bold"))
        lbl_warning.pack(padx=10, pady=5)

        self.after(1000, warning.destroy)

    #METHOD TO BUILD THE WHOLE HEADER

    def build_header(self):
        title_bar = ctk.CTkFrame(self.main_container, fg_color="transparent", height=35)
        title_bar.pack(fill="x", padx=10, pady=(8, 0))

        lbl_title = ctk.CTkLabel(title_bar, text="Auto Clicker Pro", font=("Arial", 13, "bold"), text_color=Colors.TEXT_TITLE)
        lbl_title.pack(side="left", padx=10)


        self.btn_config = ctk.CTkButton(title_bar, text="⚙", font=("Segoe UI Symbol", 16), height=14, width=14, corner_radius=6, fg_color="transparent", hover_color=Colors.BTN_HOVER, text_color=Colors.TEXT_TITLE, command=self.open_settings)
        self.btn_config.place(relx=0.25, rely=-0.063)


        self.lbl_status = ctk.CTkLabel(title_bar, text="STOPPED", width=100, font=("Arial", 14, "bold"), text_color=Colors.BORDER_LASER_STOPPED, anchor="w")
        self.lbl_status.pack(side="left", padx=(90,0))

        self.main_container.enable_drag_on(title_bar)
        self.main_container.enable_drag_on(lbl_title)
        self.main_container.enable_drag_on(self.lbl_status)
        self.main_container.enable_drag_on(self.btn_config)

        window_controls = ctk.CTkFrame(title_bar, fg_color="transparent")
        window_controls.pack(side="right")

        btn_minimize = ctk.CTkButton(window_controls, text="─", width=28, height=28, corner_radius=14,fg_color=Colors.BTN_HOVER, hover_color=Colors.BTN_HOVER, text_color=Colors.TEXT_NORMAL, command=self.minimize_window)
        btn_minimize.pack(side="left", padx=(0, 6))

        btn_close = ctk.CTkButton(window_controls, text="✕", width=28, height=28, corner_radius=14, fg_color=Colors.BTN_HOVER, hover_color=Colors.WARNING_BG, text_color=Colors.TEXT_NORMAL, command=self.destroy)
        btn_close.pack(side="left")

    #METHOD TO OPEN THE SETTINGS MENU

    def open_settings(self):
        if self.is_settings_open:
            return

        self.btn_start.configure(state="disabled")
        self.settings_win = SettingsView(master_container=self.main_container, master_view=self)
        self.settings_win.place(relx=0.17, rely=0.395, anchor="center")
        self.settings_win.lift()


    #METHOD TO GET THE TASKBAR ICON WORKING WITH THE CUSTOM HEADER

    def set_taskbar_icon(self):
        try:
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            GWL_EXSTYLE = -20
            WS_EX_APPWINDOW = 0x00040000
            WS_EX_TOOLWINDOW = 0x00000080
            style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
            style = style & ~WS_EX_TOOLWINDOW
            style = style | WS_EX_APPWINDOW
            ctypes.windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
            self.withdraw()
            self.deiconify()
        except Exception:
            pass

    #METHOD TO MINIMIZE THE WINDOW WITH THE CUSTOM HEADER

    def minimize_window(self):
        self.withdraw()
        self.overrideredirect(False)
        self.iconify()
        self.bind("<Map>", self.on_deiconify)

    def on_deiconify(self, event=None):
        self.unbind("<Map>")
        self.overrideredirect(True)
        self.after(10, self.set_taskbar_icon)

    #METHOD TO APPLY THE DYNAMIC BORDER

    def apply_border(self, show_border):
        self.show_border_active = show_border

        if show_border:
            self.main_container.configure(border_width=1)
        else:
            self.main_container.configure(border_width=0)

    #METHOD TO APPLY TOPMOST

    def apply_topmost(self, is_topmost):
        self.attributes("-topmost", is_topmost)

    #METHOD TO APPLY THE DARK/LIGHT THEME MODE

    def apply_theme(self, is_dark):
        if is_dark:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    #METHOD TO ANIMATE THE STATUS AND THE DYNAMIC BORDER

    def animated_status(self):
        if not self.running_state:
            return

        animated_lst = ["RUNNING.", "RUNNING..", "RUNNING..."]
        text_index = (self.status_index // 4) % len(animated_lst)

        if getattr(self, "show_border_active", True):
            laser_colors = ["#00ff9f", "#00ffd5", "#00f7ff", "#00c3ff", "#008cff", "#006eff", "#008cff", "#00c3ff", "#00f7ff", "#00ffd5"]
            current_laser_color = laser_colors[self.status_index % len(laser_colors)]

            self.main_container.configure(border_color=current_laser_color)
            self.lbl_status.configure(text=animated_lst[text_index], text_color=current_laser_color)
        else:
            self.lbl_status.configure(text=animated_lst[text_index], text_color="#00ff9f")

        self.status_index += 1
        self.after(100, self.animated_status)

    #METHOD TO UPDATE THE STATUS

    def update_status(self, running):
        self.running_state = running

        if running:
            self.status_index = 0
            self.btn_start.configure(state="disabled")
            self.btn_stop.configure(state="normal")
            self.btn_config.configure(state="disabled")
            self.animated_status()
        else:
            self.lbl_status.configure(text="STOPPED", text_color=Colors.BORDER_LASER_STOPPED)
            self.main_container.configure(border_color=Colors.BORDER_LASER_STOPPED)
            self.btn_start.configure(state="normal")
            self.btn_stop.configure(state="disabled")
            self.btn_config.configure(state="normal")

    #METHOD TO VALIDATE IF THE TEXT IS NUMBER OR NOT

    def validate_number(self, text):
        if text == "" or text.isdigit():
            return True
        
        self.winfo_toplevel().show_warning("ONLY NUMBERS!")
        return False

    def show_tooltip(self):
        self.tooltip.deiconify()

    def hide_tooltip(self):
        self.tooltip.withdraw()

    def update_tooltip_pos(self, x, y):
        self.tooltip_label.config(text=f"X: {int(x)} | Y: {int(y)}")
        self.tooltip.geometry(f"+{int(x) + 15}+{int(y) + 15}")