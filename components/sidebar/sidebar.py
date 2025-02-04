import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from utils.styles import BUTTON_BG_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#293643", width=70, corner_radius=0)
        self.app = app  # Reference to main application

        self.pack(side="left", fill="y")

        # Profile Image
        image = Image.open("assets/user.png").resize((50, 50))
        profile_image = CTkImage(light_image=image, size=(50, 50))
        profile_label = ctk.CTkLabel(self, image=profile_image, text="User", compound="top", text_color="white")
        profile_label.pack(pady=20)

        # Sidebar Buttons
        buttons = [
            ("Tasks", self.app.show_tasks),
            ("Profile", self.app.show_profile),
            ("Settings", self.app.show_settings),
        ]
        for btn_name, command in buttons:
            btn = ctk.CTkButton(
                self,
                text=btn_name,
                fg_color=BUTTON_BG_COLOR,
                text_color=TEXT_COLOR,
                hover_color=BUTTON_HOVER_COLOR,
                font=("Roboto", 14),
                command=command,
                corner_radius=8,
                width=60,
            )
            btn.pack(pady=10)

        # Sign Out Button
        sign_out_button = ctk.CTkButton(
            self,
            text="Sign Out",
            fg_color="#ef4444",
            text_color=TEXT_COLOR,
            hover_color="#dc2626",
            font=("Roboto", 14),
            command=self.app.sign_out,
            corner_radius=8,
            width=60,
        )
        sign_out_button.pack(side="bottom", pady=20)
