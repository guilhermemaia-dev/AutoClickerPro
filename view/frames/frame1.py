import customtkinter as ctk

class Frame1(ctk.CTkFrame):
    def __init__(self, master, click_option_var, getters_box_color, **kwargs):
        super().__init__(master, fg_color="#191729", corner_radius=12, **kwargs)
        self.click_option = click_option_var

        validate_cmd = (self.register(self.validate_number), "%P")

        self.radioButton1 = ctk.CTkRadioButton(self, text=None, variable=self.click_option, value="true", border_width_checked=3, border_width_unchecked=3, border_color="#b1a6c7", fg_color="#1f6aa5", width=25, radiobutton_width=20, radiobutton_height=20)
        self.radioButton1.grid(row=0, column=0, padx=(10,8), pady=15, sticky="w")

        self.entry_hour = ctk.CTkEntry(self, width=60, justify="center", border_width=0, corner_radius=10, validate="key", validatecommand=validate_cmd, fg_color=getters_box_color)
        self.entry_hour.grid(row=0, column=1, padx=(0,4), pady=15)
        self.entry_hour.insert(0, 0)
        lbl_entry_hour = ctk.CTkLabel(self, text="Hours")
        lbl_entry_hour.grid(row=0, column=2, padx=(0,12), pady=15)

        self.entry_mins = ctk.CTkEntry(self, width=60, justify="center", border_width=0, corner_radius=10, validate="key", validatecommand=validate_cmd, fg_color=getters_box_color)
        self.entry_mins.grid(row=0, column=3, padx=(0,4), pady=15)
        self.entry_mins.insert(0, 0)
        lbl_entry_mins = ctk.CTkLabel(self, text="Mins")
        lbl_entry_mins.grid(row=0, column=4, padx=(0,12), pady=15)

        self.entry_secs = ctk.CTkEntry(self, width=60, justify="center", border_width=0, corner_radius=10, validate="key", validatecommand=validate_cmd, fg_color=getters_box_color)
        self.entry_secs.grid(row=0, column=5, padx=(0,4), pady=15)
        self.entry_secs.insert(0, 0)
        lbl_entry_secs = ctk.CTkLabel(self, text="Secs")
        lbl_entry_secs.grid(row=0, column=6, padx=(0,12), pady=15)

        self.entry_millis = ctk.CTkEntry(self, width=60, justify="center", border_width=0, corner_radius=10, validate="key", validatecommand=validate_cmd, fg_color=getters_box_color)
        self.entry_millis.grid(row=0, column=7, padx=(0,4), pady=15)
        self.entry_millis.insert(0, 100)
        lbl_entry_millis = ctk.CTkLabel(self, text="Millis.")
        lbl_entry_millis.grid(row=0, column=8, padx=(0,12), pady=15)


        self.radioButton2 = ctk.CTkRadioButton(self, text="Random Click Interval Between", variable=self.click_option, value="false", border_width_checked=3, border_width_unchecked=3, border_color="#b1a6c7", fg_color="#1f6aa5", width=25, radiobutton_width=20, radiobutton_height=20)
        self.radioButton2.grid(row=1, column=0, padx=(10,8), pady=15, sticky="w", columnspan=8)

        self.entry_random_millis_start = ctk.CTkEntry(self, width=60, justify="center", border_width=0, corner_radius=10, validate="key", validatecommand=validate_cmd, fg_color=getters_box_color)
        self.entry_random_millis_start.grid(row=1, column=5, padx=(0,4), pady=15)
        self.entry_random_millis_start.insert(0, 100)
        lbl_entry_random_millis_start = ctk.CTkLabel(self, text="Millis.")
        lbl_entry_random_millis_start.grid(row=1, column=6, padx=(0,12), pady=15)

        self.entry_random_millis_end = ctk.CTkEntry(self, width=60, justify="center", border_width=0, corner_radius=10, validate="key", validatecommand=validate_cmd, fg_color=getters_box_color)
        self.entry_random_millis_end.grid(row=1, column=7, padx=(0,4), pady=15)
        self.entry_random_millis_end.insert(0, 200)
        lbl_entry_random_millis_end = ctk.CTkLabel(self, text="Millis.")
        lbl_entry_random_millis_end.grid(row=1, column=8, padx=(0,12), pady=15)


    def validate_number(self, text):
        if text == "" or text.isdigit():
            return True
        
        self.winfo_toplevel().show_warning("ONLY NUMBERS!")
        return False

        