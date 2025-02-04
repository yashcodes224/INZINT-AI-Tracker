import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from components.settings.settings import SettingsSection
from components.profile.profile import ProfileUI
from components.tasks.tasks import TasksSection
from components.timer import TimerMixin
from components.sidebar.sidebar import Sidebar
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

        self.sidebar = Sidebar(self, self)

        # Left Section (Tasks, Profile, Settings) - 50% Width
        self.left_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR, corner_radius=0)
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.left_frame.pack_propagate(False)

        # Right Section (Timer) - 50% Width
        self.right_frame = ctk.CTkFrame(self, fg_color="#f6f9fb", corner_radius=0)
        self.right_frame.pack(side="right", fill="both", expand=True)
        self.right_frame.pack_propagate(False)

        # Load Initial Page (Tasks)
        self.show_tasks()

        # Create Timer UI (This stays unchanged)
        self.create_timer_section(self.right_frame)


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

