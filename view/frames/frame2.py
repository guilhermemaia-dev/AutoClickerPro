import customtkinter as ctk

class Frame2(ctk.CTkFrame):
    def __init__(self, master, repeat_til_stopped_var, getters_box_color, **kwargs):
        super().__init__(master, fg_color="#191729", corner_radius=12, height=80, **kwargs)
        self.repeat_til_stopped = repeat_til_stopped_var
        self.getters_box_color = getters_box_color

        self.selected_key = None


        top_window = self.winfo_toplevel()
        validate_cmd = (self.register(top_window.validate_number), "%P")

        self.mode_select = ctk.CTkOptionMenu(self, values=["Mouse", "Keyboard"], width=95, fg_color=getters_box_color, button_color=getters_box_color, button_hover_color=getters_box_color, corner_radius=10, command=self.on_mode_change)
        self.mode_select.grid(row=0, column=0, padx=(5,0), pady=8, sticky="w")
        self.mode_select.set("Mouse")



        self.mouse_button_select = ctk.CTkOptionMenu(self, values=["Left", "Right", "Middle"], width=95, fg_color=getters_box_color, button_color=getters_box_color, button_hover_color=getters_box_color, corner_radius=10)
        self.mouse_button_select.grid(row=0, column=1, padx=10, pady=8)
        self.mouse_button_select.set("Left")
    

        self.lbl_click_type = ctk.CTkLabel(self, text="Click type")
        self.lbl_click_type.grid(row=1, column=0, padx=(10,0), pady=8, sticky="w")

        self.click_type = ctk.CTkOptionMenu(self, values=["Single", "Double"], width=95, fg_color=getters_box_color, button_color=getters_box_color, button_hover_color=getters_box_color, corner_radius=10)
        self.click_type.grid(row=1, column=1, padx=10, pady=8)
        self.click_type.set("Single")


        self.btn_key_binder = ctk.CTkButton(self, text="Key: Select Key", width=95, corner_radius=10, fg_color=getters_box_color, hover_color="#2b2640", command=self.start_listening_key)



        self.radioButton3 = ctk.CTkRadioButton(self, text="Repeat", variable=self.repeat_til_stopped, value="false", border_width_checked=3, border_width_unchecked=3, border_color="#b1a6c7", fg_color="#1f6aa5", width=25, radiobutton_width=20, radiobutton_height=20)
        self.radioButton3.grid(row=0, column=2, padx=(0,4), pady=8, sticky="w")

        self.entry_repeat_times = ctk.CTkEntry(self, width=60, justify="center", border_width=0, corner_radius=10, validate="key", validatecommand=validate_cmd, fg_color=getters_box_color)
        self.entry_repeat_times.grid(row=0, column=3, padx=(0,2), pady=8, sticky="w")
        self.entry_repeat_times.insert(0, 0)

        lbl_entry_repeat_times = ctk.CTkLabel(self, text="Times")
        lbl_entry_repeat_times.grid(row=0, column=4, padx=(2,0), pady=8, sticky="w")


        self.radioButton4 = ctk.CTkRadioButton(self, text="Repeat Until Stopped", variable=self.repeat_til_stopped, value="true", border_width_checked=3, border_width_unchecked=3, border_color="#b1a6c7", fg_color="#1f6aa5", width=25, radiobutton_width=20, radiobutton_height=20)
        self.radioButton4.grid(row=1, column=2, columnspan=2, padx=(0,10), pady=8, sticky="w")


        self.lbl_clicks_counter = ctk.CTkLabel(self, text="Clicks: 0", font=("Arial", 11, "bold"), text_color="#b1a6c7", width=80, anchor="w")
        self.lbl_clicks_counter.grid(row=1, column=4, padx=(6,10), pady=8, sticky="w")

        lbl_action_type = ctk.CTkLabel(self, text="Mode")
        lbl_action_type.grid(row=2, column=0, padx=(10,0), pady=8, sticky="w")

        self.action_type = ctk.CTkOptionMenu(self, values=["Click", "Hold"], width=95, fg_color=getters_box_color, button_color=getters_box_color, corner_radius=10)
        self.action_type.grid(row=2, column=1, padx=10, pady=8)
        self.action_type.set("Click")


    def on_mode_change(self, mode):
        top_window = self.winfo_toplevel()
        top_window.unbind("<Key>")
        if mode == "Mouse":
            self.btn_key_binder.grid_forget()
            self.mouse_button_select.grid(row=0, column=1, padx=5, pady=8)
            self.lbl_click_type.grid(row=1, column=0, padx=(5,0), pady=8, sticky="w")
            self.click_type.grid(row=1, column=1, padx=10, pady=8)
        else:
            self.mouse_button_select.grid_forget()
            self.lbl_click_type.grid_forget()
            self.click_type.grid_forget()
            self.btn_key_binder.grid(row=0, column=1, padx=10, pady=8)


    def start_listening_key(self):
        self.btn_key_binder.configure(text="Press Any Key...", fg_color="#3b3355")
        top_window = self.winfo_toplevel()
        top_window.bind("<Key>", self.on_key_captured)

    def on_key_captured(self, event):
        top_window = self.winfo_toplevel()
        top_window.unbind("<Key>")

        key_name = event.keysym.lower()

        if key_name == "f6":
            self.selected_key = None
            self.btn_key_binder.configure(text="Key: Select Key", fg_color=self.getters_box_color)
            top_window.show_warning("F6 IS RESERVED!")
            return

        self.selected_key = key_name
        self.btn_key_binder.configure(text=f"Key: {key_name.capitalize()}", fg_color=self.getters_box_color)
        


    def update_click_display(self, count):
        if count >= 1_000_000:
            formatted_count = f"{count / 1_000_000:.1f}M"
        elif count >= 10_000:
            formatted_count = f"{count / 1_000:.1f}k"
        else:
            formatted_count = str(count)

        self.lbl_clicks_counter.configure(text=f"Clicks: {formatted_count}")