import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from components.sidebar.sidebar_style import LIGHT_THEME, DARK_THEME  # Import styles

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, app):
        self.app = app  # Reference to main application
        self.theme = LIGHT_THEME if app.current_theme == "Light" else DARK_THEME  # Apply theme

        super().__init__(parent, fg_color=self.theme["bg_color"], width=self.theme["sidebar_width"], corner_radius=0)  

        self.pack(side="left", fill="y")
        self.pack_propagate(False)
        self.create_widgets()

    def create_widgets(self):
        """Create the sidebar UI elements with .ico icons."""
        # Profile Image
        profile_image = CTkImage(light_image=Image.open("assets/logo3.ico").resize((45, 45)), size=(45, 45))
        profile_label = ctk.CTkLabel(self, image=profile_image, text="", text_color=self.theme["text_color"])
        profile_label.pack(pady=12)

        # Sidebar Buttons with Icons
        buttons = [
            ("tasks", "Tasks", self.app.show_tasks),
            ("profile", "Profile", self.app.show_profile),
            ("settings", "Settings", self.app.show_settings),
        ]

        for icon_key, btn_name, command in buttons:
            icon_path = self.theme["icons"][icon_key]  # Get correct icon based on theme
            icon_image = CTkImage(light_image=Image.open(icon_path), size=(30, 30))  # Bigger icon

            btn = ctk.CTkButton(
                self,
                image=icon_image,
                text=btn_name,
                fg_color="transparent",
                text_color=self.theme["text_color"],
                hover_color=self.theme["button_hover"],
                font=("Roboto", 10),  # Small text
                command=command,
                corner_radius=8,
                width=60,
                height=75,
                compound="top",  # Icon on top, text below
            )
            btn.pack(pady=15)

        # Sign Out Button (Same Icon for Both Themes)
        logout_icon = CTkImage(light_image=Image.open(self.theme["icons"]["logout"]), size=(30, 30))
        sign_out_button = ctk.CTkButton(
            self,
            image=logout_icon,
            text="Sign Out",
            fg_color=self.theme["button_bg"],
            text_color="white",
            hover_color=self.theme["button_hover"],
            font=("Roboto", 10),  # Small text
            command=self.app.sign_out,
            corner_radius=8,
            width=60,
            height=75,
            compound="top",
        )
        sign_out_button.pack(side="bottom", pady=15)

    def apply_theme(self):
        """Apply theme dynamically when changed."""
        self.theme = LIGHT_THEME if self.app.current_theme == "Light" else DARK_THEME
        self.configure(fg_color=self.theme["bg_color"], width=self.theme["sidebar_width"])
        
        # Update all buttons dynamically
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(fg_color="transparent", text_color=self.theme["text_color"], hover_color=self.theme["button_hover"])