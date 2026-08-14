import customtkinter as ctk
import config
from view.components.theme import Colors

class Frame2(ctk.CTkFrame):
    def __init__(self, master, repeat_mode_var, location_mode_var, **kwargs):
        super().__init__(master, fg_color=Colors.BG_FRAME, corner_radius=12, height=80, **kwargs)
        self.repeat_mode = repeat_mode_var
        self.location_mode = location_mode_var
        self.selected_key = None

        top_window = self.winfo_toplevel()
        validate_cmd = (self.register(top_window.validate_number), "%P")


        #MENU TO SELECT BETWEEN MOUSE AND KEYBOARD
        self.mode_select = ctk.CTkOptionMenu(self, values=["Mouse", "Keyboard"], width=95, fg_color=Colors.BOX_COLOR, button_color=Colors.BOX_COLOR, button_hover_color=Colors.BOX_HOVER, corner_radius=10, text_color=Colors.TEXT_NORMAL, dropdown_fg_color=Colors.BG_FRAME, dropdown_text_color=Colors.TEXT_NORMAL, command=self.on_mode_change)
        self.mode_select.grid(row=0, column=0, padx=(5,0), pady=8, sticky="w")
        self.mode_select.set("Mouse")


        #MENU TO SELECT BETWEEN LEFT, RIGHT AND MIDDLE
        self.mouse_button_select = ctk.CTkOptionMenu(self, values=["Left", "Right", "Middle"], width=95, fg_color=Colors.BOX_COLOR, button_color=Colors.BOX_COLOR, button_hover_color=Colors.BOX_HOVER, corner_radius=10, text_color=Colors.TEXT_NORMAL, dropdown_fg_color=Colors.BG_FRAME, dropdown_text_color=Colors.TEXT_NORMAL)
        self.mouse_button_select.grid(row=0, column=1, padx=10, pady=8)
        self.mouse_button_select.set("Left")
    

        #MENU TO SELECT THE CLICK OPTION (SINGLE OR DOUBLE)
        self.lbl_click_type = ctk.CTkLabel(self, text="Click type", text_color=Colors.TEXT_NORMAL)
        self.lbl_click_type.grid(row=1, column=0, padx=(10,8), pady=8, sticky="w")

        self.click_type = ctk.CTkOptionMenu(self, values=["Single", "Double"], width=95, fg_color=Colors.BOX_COLOR, button_color=Colors.BOX_COLOR, button_hover_color=Colors.BOX_HOVER, corner_radius=10, text_color=Colors.TEXT_NORMAL, dropdown_fg_color=Colors.BG_FRAME, dropdown_text_color=Colors.TEXT_NORMAL)
        self.click_type.grid(row=1, column=1, padx=10, pady=8)
        self.click_type.set("Single")


        #BUTTON TO SELECT THE KEY
        self.btn_key_binder = ctk.CTkButton(self, text="Key: Select Key", width=95, corner_radius=10, fg_color=Colors.BOX_COLOR, hover_color=Colors.BOX_HOVER, command=self.start_listening_key, text_color=Colors.TEXT_NORMAL)



        # REPEAT MODE - TIMES
        self.radioButton3 = ctk.CTkRadioButton(self, text="Repeat", variable=self.repeat_mode, value="times", border_width_checked=2, border_width_unchecked=2, border_color=Colors.TEXT_TITLE, fg_color=Colors.RADIO_BTN, text_color=Colors.TEXT_NORMAL, width=25, radiobutton_width=20, radiobutton_height=20)
        self.radioButton3.grid(row=0, column=2, padx=(0,4), pady=8, sticky="w")

        self.entry_repeat_times = ctk.CTkEntry(self, width=60, justify="center", border_width=0, corner_radius=10, validate="key", validatecommand=validate_cmd, fg_color=Colors.BOX_COLOR)
        self.entry_repeat_times.grid(row=0, column=3, padx=(0,2), pady=8, sticky="w")
        self.entry_repeat_times.insert(0, 0)

        lbl_entry_repeat_times = ctk.CTkLabel(self, text="Times", text_color=Colors.TEXT_NORMAL)
        lbl_entry_repeat_times.grid(row=0, column=4, padx=(2,0), pady=8, sticky="w")



        # REPEAT MODE - UNTIL STOPPED
        self.radioButton4 = ctk.CTkRadioButton(self, text="Repeat Until Stopped", variable=self.repeat_mode, value="until_stopped", border_width_checked=2, border_width_unchecked=2, border_color=Colors.TEXT_TITLE, fg_color=Colors.RADIO_BTN, text_color=Colors.TEXT_NORMAL, width=25, radiobutton_width=20, radiobutton_height=20)
        self.radioButton4.grid(row=1, column=2, columnspan=2, padx=(0,6), pady=8, sticky="w")


        # LABEL TO DISPLAY THE NUMBER OF CLICKS
        self.lbl_clicks_counter = ctk.CTkLabel(self, text="Clicks: 0", font=("Arial", 10, "bold"), text_color=Colors.TEXT_TITLE, anchor="w")
        self.lbl_clicks_counter.grid(row=1, column=4, padx=(0,10), pady=8, sticky="w")


        # MENU TO SELECT THE CLICK MODE (CLICK OR HOLD)
        lbl_action_type = ctk.CTkLabel(self, text="Mode", text_color=Colors.TEXT_NORMAL)
        lbl_action_type.grid(row=2, column=0, padx=(10,0), pady=8, sticky="w")

        self.action_type = ctk.CTkOptionMenu(self, values=["Click", "Hold"], width=95, fg_color=Colors.BOX_COLOR, button_color=Colors.BOX_COLOR, corner_radius=10, button_hover_color=Colors.BOX_HOVER, text_color=Colors.TEXT_NORMAL, dropdown_fg_color=Colors.BG_FRAME, dropdown_text_color=Colors.TEXT_NORMAL)
        self.action_type.grid(row=2, column=1, padx=10, pady=8)
        self.action_type.set("Click")


        # REPEAT MODE - TIMER
        self.radioButton5 = ctk.CTkRadioButton(self, text="Timer", variable=self.repeat_mode, value="timer", border_width_checked=2, border_width_unchecked=2, border_color=Colors.TEXT_TITLE, fg_color=Colors.RADIO_BTN, text_color=Colors.TEXT_NORMAL, width=25, radiobutton_width=20, radiobutton_height=20)
        self.radioButton5.grid(row=2, column=2, columnspan=2, padx=(0,10), pady=8, sticky="w")


        self.entry_timer = ctk.CTkEntry(self, width=75, justify="center", border_width=0, corner_radius=10, fg_color=Colors.BOX_COLOR, text_color=Colors.TEXT_NORMAL, font=("Consolas", 11, "bold"))
        self.entry_timer.grid(row=2, column=3, columnspan=2, padx=(0,10), pady=8, sticky="w")
        self.entry_timer.insert(0, "00:00:00")
        self.entry_timer.bind("<KeyRelease>", self.format_timer_input)


        # CHOOSE LOCATION
        #CURRENT LOCATION
        self.radioButton6 = ctk.CTkRadioButton(self, text="Current Location", variable=self.location_mode, value="current", border_width_checked=2, border_width_unchecked=2, border_color=Colors.TEXT_TITLE, fg_color=Colors.RADIO_BTN, text_color=Colors.TEXT_NORMAL, width=25, radiobutton_width=20, radiobutton_height=20)
        self.radioButton6.grid(row=3, column=0, padx=(10,8), pady=8, sticky="w")

        # SPECIFIC LOCATION
        self.radioButton7 = ctk.CTkRadioButton(self, text=None, variable=self.location_mode, value="specific", border_width_checked=2, border_width_unchecked=2, border_color=Colors.TEXT_TITLE, fg_color=Colors.RADIO_BTN, width=25, radiobutton_width=20, radiobutton_height=20)
        self.radioButton7.grid(row=3, column=1, padx=(10,2), pady=8, sticky="e")

        # GET THE COORDS
        self.btn_get_coords = ctk.CTkButton(self, text="Get", width=55, corner_radius=10, fg_color=Colors.BOX_COLOR, hover_color=Colors.BOX_HOVER, text_color=Colors.TEXT_NORMAL)
        self.btn_get_coords.grid(row=3, column=2, padx=(0,0), pady=8, sticky="w")

        lbl_coords_X = ctk.CTkLabel(self, text="X", text_color=Colors.TEXT_NORMAL)
        lbl_coords_X.grid(row=3, column=2, padx=(0,4), pady=8, sticky="e")
        self.entry_coords_x = ctk.CTkEntry(self, width=55, justify="center", border_width=0, corner_radius=10, validate="key", validatecommand=validate_cmd, fg_color=Colors.BOX_COLOR, text_color=Colors.TEXT_NORMAL)
        self.entry_coords_x.grid(row=3, column=3, padx=(2,0), pady=8, sticky="w")

        lbl_coords_Y = ctk.CTkLabel(self, text="Y", text_color=Colors.TEXT_NORMAL)
        lbl_coords_Y.grid(row=3, column=3, padx=(0,4), pady=8, sticky="e")
        self.entry_coords_y = ctk.CTkEntry(self, width=55, justify="center", border_width=0, corner_radius=10, validate="key", validatecommand=validate_cmd, fg_color=Colors.BOX_COLOR, text_color=Colors.TEXT_NORMAL)
        self.entry_coords_y.grid(row=3, column=4, padx=(2,2), pady=8, sticky="w")


    #METHOD TO FORMAT THE TIMER INPUT
    def format_timer_input(self,event):
        text = self.entry_timer.get()
        digits = "".join(filter(str.isdigit, text))[-6:]
        padded = digits.zfill(6)
        formatted = f"{padded[:2]}:{padded[2:4]}:{padded[4:]}"

        self.entry_timer.delete(0, "end")
        self.entry_timer.insert(0, formatted)

    def get_timer_secs(self):
        text = self.entry_timer.get()
        digits = "".join(filter(str.isdigit, text)).zfill(6)
        h = int(digits[:2])
        m = int(digits[2:4])
        s = int(digits[4:])
        return (h*3600) + (m*60) + s

    def update_timer_display(self, tot_secs):
        hours = tot_secs // 3600
        minutes = (tot_secs % 3600) // 60
        seconds = tot_secs % 60

        formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        self.entry_timer.delete(0, "end")
        self.entry_timer.insert(0, formatted)


    #METHOD TO DISPLAY THE CURRENT MODE SELECTED
    def on_mode_change(self, mode):
        top_window = self.winfo_toplevel()
        top_window.unbind("<Key>")
        if mode == "Mouse":
            self.btn_key_binder.grid_forget()
            self.mouse_button_select.grid(row=0, column=1, padx=5, pady=8)
        else:
            self.mouse_button_select.grid_forget()
            self.btn_key_binder.grid(row=0, column=1, padx=10, pady=8)

        self.lbl_click_type.grid(row=1, column=0, padx=(5,0), pady=8, sticky="w")
        self.click_type.grid(row=1, column=1, padx=10, pady=8)


    def start_listening_key(self):
        self.btn_key_binder.configure(text="Press Any Key...", fg_color=Colors.BTN_ACTIVE_KEY)
        top_window = self.winfo_toplevel()
        top_window.bind("<Key>", self.on_key_captured)

    def on_key_captured(self, event):
        top_window = self.winfo_toplevel()
        top_window.unbind("<Key>")

        key_name = event.keysym.lower()
        current_configs = config.load_settings()
        reserved_key = current_configs.get("hotkey", "F6").lower()

        if key_name == reserved_key:
            self.selected_key = None
            self.btn_key_binder.configure(text="Key: Select Key", fg_color=Colors.BOX_COLOR)
            top_window.show_warning(f"{reserved_key.upper()} IS RESERVED!")
            return

        self.selected_key = key_name
        self.btn_key_binder.configure(text=f"Key: {key_name.capitalize()}", fg_color=Colors.BOX_COLOR)


    def apply_clicks(self, show_clicks):
        self.show_clicks_active = show_clicks

        if show_clicks:
            self.lbl_clicks_counter.grid()
        else:
            self.lbl_clicks_counter.grid_remove()

    def update_click_display(self, count):
        if not getattr(self, "show_clicks_active", True):
            return
        
        if count >= 1_000_000_000:
            formatted_count = f"{count / 1_000_000_000:.1f}B"
        elif count >= 1_000_000:
            formatted_count = f"{count / 1_000_000:.1f}M"
        elif count >= 1_000:
            formatted_count = f"{count / 1_000:.1f}k"
        else:
            formatted_count = str(count)

        formatted_count = formatted_count.replace(".0", "")
        self.lbl_clicks_counter.configure(text=f"Clicks: {formatted_count}")