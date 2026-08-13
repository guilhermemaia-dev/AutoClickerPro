import customtkinter as ctk
import tkinter as tk
from view.components.main_window_frame import MainWindowFrame
from view.frames.frame1 import Frame1
from view.frames.frame2 import Frame2
from view.frames.frame3 import Frame3
from view.settings_view import SettingsView
import ctypes

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainView(ctk.CTk):
    def __init__(self, controller=None):
        super().__init__()

        self.controller = controller

        self.overrideredirect(True)
        self.title("Auto Clicker Pro")
        self.geometry("500x400")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color="#000001")
        self.wm_attributes("-transparentcolor", "#000001")
        try:
            self.iconbitmap("assets/autoclicker.ico")
        except Exception:
            pass

        self.click_option = ctk.StringVar(value="true")
        self.repeat_mode = ctk.StringVar(value="until_stopped")
        self.location_mode = ctk.StringVar(value="current")

        self.main_container = MainWindowFrame(self, window=self, corner_radius=12, border_width=1, border_color="#ff4757", fg_color="#171427")
        self.main_container.pack(fill="both", expand=True)

        self.build_header()

        self.getters_box_color = "#313038"

        self.frame1 = Frame1(self.main_container, click_option_var=self.click_option, getters_box_color=self.getters_box_color)
        self.frame1.pack(side="top", fill="x", padx=15, pady=4)

        self.frame2 = Frame2(self.main_container, repeat_mode_var=self.repeat_mode, location_mode_var=self.location_mode, getters_box_color=self.getters_box_color)
        self.frame2.pack(side="top", fill="x", padx=15, pady=4)

        self.frame3 = Frame3(self.main_container)
        self.frame3.pack(side="top", fill="x", padx=15, pady=4)

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


    def show_warning(self, message):
        warning = ctk.CTkFrame(self.main_container, fg_color="#f34b59", corner_radius=8)
        warning.place(relx=0.55, rely=0.055, anchor="center")

        warning.lift()

        lbl_warning = ctk.CTkLabel(warning, text=message, text_color="white", font=("Arial", 11, "bold"))
        lbl_warning.pack(padx=10, pady=5)

        self.after(1000, warning.destroy)


    def build_header(self):
        title_bar = ctk.CTkFrame(self.main_container, fg_color="transparent", height=35)
        title_bar.pack(fill="x", padx=10, pady=(8, 0))

        lbl_title = ctk.CTkLabel(title_bar, text="Auto Clicker Pro", font=("Arial", 13, "bold"), text_color="#b1a6c7")
        lbl_title.pack(side="left", padx=10)


      
        self.btn_config = ctk.CTkButton(title_bar, text="⚙", font=("Segoe UI Symbol", 16), height=14, width=14, corner_radius=6, fg_color="transparent", hover_color="#27243F", command=self.open_settings)
        self.btn_config.pack(side="left", padx=5)



        self.lbl_status = ctk.CTkLabel(title_bar, text="STOPPED", font=("Arial", 14, "bold"), text_color="#e44949", anchor="w")
        self.lbl_status.pack(side="left", padx=(60,0))

        self.main_container.enable_drag_on(title_bar)
        self.main_container.enable_drag_on(lbl_title)
        self.main_container.enable_drag_on(self.lbl_status)
        self.main_container.enable_drag_on(self.btn_config)

        window_controls = ctk.CTkFrame(title_bar, fg_color="transparent")
        window_controls.pack(side="right")

        btn_minimize = ctk.CTkButton(window_controls, text="─", width=28, height=28, corner_radius=14,fg_color="#27243F", hover_color="#3b3759", command=self.minimize_window)
        btn_minimize.pack(side="left", padx=(0, 6))

        btn_close = ctk.CTkButton(window_controls, text="✕", width=28, height=28, corner_radius=14, fg_color="#27243F", hover_color="#ff4757", command=self.destroy)
        btn_close.pack(side="left")


    def open_settings(self):
        if self.is_settings_open:
            return

        self.btn_start.configure(state="disabled")
        self.settings_win = SettingsView(master_container=self.main_container, master_view=self, getters_box_color=self.getters_box_color)
        self.settings_win.place(relx=0.17, rely=0.395, anchor="center")
        self.settings_win.lift()


    # method to get the taskbar icon working with the custom header
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

    def minimize_window(self):
        self.withdraw()
        self.overrideredirect(False)
        self.iconify()
        self.bind("<Map>", self.on_deiconify)

    def on_deiconify(self, event=None):
        self.unbind("<Map>")
        self.overrideredirect(True)
        self.after(10, self.set_taskbar_icon)

    def apply_border(self, show_border):
        self.show_border_active = show_border

        if show_border:
            self.main_container.configure(border_width=1)
        else:
            self.main_container.configure(border_width=0)

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

    def update_status(self, running):
        self.running_state = running

        if running:
            self.status_index = 0
            self.btn_start.configure(state="disabled")
            self.btn_stop.configure(state="normal")
            self.btn_config.configure(state="disabled")
            self.animated_status()
        else:
            self.lbl_status.configure(text="STOPPED", text_color="#e44949")
            self.main_container.configure(border_color="#ff0055")
            self.btn_start.configure(state="normal")
            self.btn_stop.configure(state="disabled")
            self.btn_config.configure(state="normal")

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