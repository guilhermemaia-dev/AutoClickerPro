import customtkinter as ctk

class Frame2(ctk.CTkFrame):
    def __init__(self, master, getters_box_color, **kwargs):
        super().__init__(master, fg_color="#191729", corner_radius=12, height=80, **kwargs)


        lbl_mouse_button = ctk.CTkLabel(self, text="Mouse Button")
        lbl_mouse_button.grid(row=0, column=0, padx=(5,0), pady=3, sticky="w")

        self.mouse_button_select = ctk.CTkOptionMenu(self, values=["Left", "Right", "Middle"], width=110, fg_color=getters_box_color, button_color=getters_box_color, button_hover_color=getters_box_color, corner_radius=10)
        self.mouse_button_select.grid(row=0, column=1, padx=10, pady=3)
        self.mouse_button_select.set("Left")
    

        lbl_click_type = ctk.CTkLabel(self, text="Click type")
        lbl_click_type.grid(row=1, column=0, padx=(5,0), pady=3, sticky="w")

        self.click_type = ctk.CTkOptionMenu(self, values=["Single", "Double"], width=110, fg_color=getters_box_color, button_color=getters_box_color, button_hover_color=getters_box_color, corner_radius=10)
        self.click_type.grid(row=1, column=1, padx=10, pady=3)
        self.click_type.set("Single")
