import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from components.settings.settings import SettingsSection
from components.profile.profile import ProfileUI
from components.tasks.tasks import TasksSection
from components.timer import TimerMixin
from utils.styles import PRIMARY_COLOR, BUTTON_BG_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR
import json
import os


class TrackerApp(ctk.CTk, TimerMixin):
    def __init__(self, token):
        super().__init__()
        TimerMixin.__init__(self, self)  # Initialize TimerMixin once

        self.token = token
        self.title("iTrack")
        self.geometry("770x560")
        self.resizable(False, False)
        self.task_data = []

        # Sidebar (Fixed Width)
        self.sidebar = ctk.CTkFrame(self, fg_color="#293643", width=70, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        # Left Section (Tasks, Profile, Settings) - 50% Width
        self.left_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR, corner_radius=0)
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.left_frame.pack_propagate(False)

        # Right Section (Timer) - 50% Width
        self.right_frame = ctk.CTkFrame(self, fg_color="#f6f9fb", corner_radius=0)
        self.right_frame.pack(side="right", fill="both", expand=True)
        self.right_frame.pack_propagate(False)

        # Sidebar Navigation
        self.create_sidebar()

        # Load Initial Page (Tasks)
        self.show_tasks()

        # Create Timer UI (This stays unchanged)
        self.create_timer_section(self.right_frame)


    def create_sidebar(self):
        """Create the sidebar with navigation buttons."""
        image = Image.open("assets/user.png").resize((50, 50))
        profile_image = CTkImage(light_image=image, size=(50, 50))
        profile_label = ctk.CTkLabel(self.sidebar, image=profile_image, text="User", compound="top", text_color="white")
        profile_label.pack(pady=20)

        # Sidebar Buttons
        buttons = [
            ("Tasks", self.show_tasks),
            ("Profile", self.show_profile),
            ("Settings", self.show_settings),
        ]
        for btn_name, command in buttons:
            btn = ctk.CTkButton(
                self.sidebar,
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
            self.sidebar,
            text="Sign Out",
            fg_color="#ef4444",
            text_color=TEXT_COLOR,
            hover_color="#dc2626",
            font=("Roboto", 14),
            command=self.sign_out,
            corner_radius=8,
            width=60,
        )
        sign_out_button.pack(side="bottom", pady=20)

    def clear_left_frame(self):
        """Clear only the left section while keeping the Timer UI on the right unchanged."""
        for widget in self.left_frame.winfo_children():
            widget.destroy()

    def show_profile(self):
        """Switch to Profile UI while keeping the Timer UI fixed."""
        self.clear_left_frame()
        ProfileUI(self.left_frame, self).pack(fill="both", expand=True)

    def show_tasks(self):
        """Switch to Tasks UI while keeping the Timer UI fixed."""
        self.clear_left_frame()
        TasksSection(self.left_frame, self).pack(fill="both", expand=True)

    def show_settings(self):
        """Switch to Settings UI while keeping the Timer UI fixed."""
        self.clear_left_frame()
        SettingsSection(self.left_frame, self).pack(fill="both", expand=True)

    def sign_out(self):
        """Close the application."""
        self.destroy()


if __name__ == "__main__":
    app = TrackerApp(token="your_token_here")
    app.iconbitmap('assets/logo2.ico')
    app.mainloop()

