import customtkinter as ctk
import requests
from tkinter import messagebox
from components.timer.timer import TimerMixin
from components.profile.update_profile_form import UpdateProfileForm
from components.profile.profile_style import LIGHT_THEME, DARK_THEME
from dotenv import load_dotenv
import os
import sys

# Determine the correct path for the .env file
if getattr(sys, 'frozen', False):  # If running as a bundled .exe
    env_path = os.path.join(sys._MEIPASS, '.env')  # Extracted folder path
else:
    env_path = '.env'  # If running from source, it's just the current directory

# Load the .env file
load_dotenv(env_path)

# API Endpoint
API_PROFILE_URL = "https://o9bc4pbt8b.execute-api.ap-south-1.amazonaws.com/development/profile"

class ProfileUI(ctk.CTkFrame, TimerMixin):
    def __init__(self, parent, app, token):
        super().__init__(parent)
        TimerMixin.__init__(self, app, user_name=app.user_name)

        self.app = app
        self.token = token
        self.apply_theme()
        self.configure(fg_color=self.theme["background"])

        self.left_frame = ctk.CTkFrame(
            self,
            fg_color=self.theme["left_frame"]["fg_color"],
            corner_radius=self.theme["left_frame"]["corner_radius"]
        )
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.left_frame.pack_propagate(False)

        # Initialize profile data
        self.profile_data = {
            "name": "Loading...",
            "email": "Loading...",
            "organization": "Loading..."
        }

        # Fetch profile details from API
        self.fetch_profile_data()

    def apply_theme(self):
        """Apply the selected theme (Light or Dark)."""
        self.theme = LIGHT_THEME if self.app.current_theme == "Light" else DARK_THEME
        self.configure(fg_color=self.theme["background"])

    def fetch_profile_data(self):
        """Fetch user profile details using the stored authentication token."""
        headers = {"Authorization": f"Bearer {self.app.token}"}

        try:
            response = requests.get(API_PROFILE_URL, headers=headers)

            if response.status_code == 200:
                user_data = response.json()
                self.profile_data = {
                    "name": user_data.get("name", "N/A"),
                    "email": user_data.get("email", "N/A"),
                    "organization": "Not Available"  # Modify this if your API returns organization info
                }
            else:
                messagebox.showerror("Error", "Failed to fetch profile details.")

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")

        self.show_profile_section()

    def show_profile_section(self):
        """Clear left frame and display the profile information."""
        self.clear_left_frame()

        header_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 5))

        header = ctk.CTkLabel(
            header_frame,
            text="Profile",
            font=self.theme["header"]["font"],
            text_color=self.theme["header"]["text_color"]
        )
        header.pack(side="left")

        profile_card = ctk.CTkFrame(
            self.left_frame,
            fg_color=self.theme["profile_card"]["fg_color"],
            corner_radius=self.theme["profile_card"]["corner_radius"],
            border_width=self.theme["profile_card"]["border_width"],
            border_color=self.theme["profile_card"]["border_color"]
        )
        profile_card.pack(fill="both", expand=True, padx=10, pady=10)

        profile_img = ctk.CTkLabel(
            profile_card,
            text=self.theme["profile_img"]["text"],
            font=self.theme["profile_img"]["font"],
            fg_color=self.theme["profile_img"]["fg_color"],
            text_color=self.theme["profile_img"]["text_color"],
            width=self.theme["profile_img"]["width"],
            height=self.theme["profile_img"]["height"],
            corner_radius=self.theme["profile_img"]["corner_radius"]
        )
        profile_img.pack(pady=15)

        self.username_label = ctk.CTkLabel(
            profile_card,
            text=self.profile_data["name"],
            font=self.theme["username_label"]["font"],
            text_color=self.theme["username_label"]["text_color"]
        )
        self.username_label.pack(pady=(5, 2))

        self.email_label = ctk.CTkLabel(
            profile_card,
            text=self.profile_data["email"],
            font=self.theme["email_label"]["font"],
            text_color=self.theme["email_label"]["text_color"]
        )
        self.email_label.pack(pady=5)

        self.org_label = ctk.CTkLabel(
            profile_card,
            text=f"Organization: {self.profile_data['organization']}",
            font=self.theme["org_label"]["font"],
            text_color=self.theme["org_label"]["text_color"]
        )
        self.org_label.pack(pady=5)

        divider = ctk.CTkFrame(
            profile_card,
            fg_color=self.theme["divider"]["fg_color"],
            height=self.theme["divider"]["height"]
        )
        divider.pack(fill="x", padx=20, pady=10)

        update_btn = ctk.CTkButton(
            profile_card,
            text=self.theme["update_btn"]["text"],
            font=self.theme["update_btn"]["font"],
            fg_color=self.theme["update_btn"]["fg_color"],
            hover_color=self.theme["update_btn"]["hover_color"],
            width=self.theme["update_btn"]["width"],
            height=self.theme["update_btn"]["height"],
            corner_radius=self.theme["update_btn"]["corner_radius"],
            text_color=self.theme["update_btn"]["text_color"],
            command=self.open_update_profile
        )
        update_btn.pack(pady=10)

    def open_update_profile(self):
        """Clear the left section and show the Update Profile Form."""
        self.clear_left_frame()
        UpdateProfileForm(self.left_frame, self.app, self.save_updated_profile).pack(fill="both", expand=True)

    def save_updated_profile(self, updated_data):
        """Save the updated profile data and return to the Profile page."""
        self.profile_data.update(updated_data)
        self.show_profile_section()

    def clear_left_frame(self):
        """Clear all widgets in the left frame."""
        for widget in self.left_frame.winfo_children():
            widget.destroy()
