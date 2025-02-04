import customtkinter as ctk
from PIL import Image
from components.timer import TimerMixin
from components.profile.update_profile_form import UpdateProfileForm  # Import Update Profile Form


class ProfileUI(ctk.CTkFrame, TimerMixin):
    def __init__(self, parent, app):
        super().__init__(parent)
        TimerMixin.__init__(self, app)  # Initialize TimerMixin with the app instance

        self.app = app  # Store app reference
        self.configure(fg_color="white")  # Set background to white

        # Split into two sections: Profile (Left) & Timer (Right)
        self.left_frame = ctk.CTkFrame(self, fg_color="#f2f4f7", corner_radius=0)
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.left_frame.pack_propagate(False)

        # Profile Information (Initially Displayed)
        self.profile_data = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "organization": "Acme Corp"
        }

        # Show Profile Section
        self.show_profile_section()

    def show_profile_section(self):
        """Clear left frame and display the profile information."""
        self.clear_left_frame()

        # Header
        header_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 5))

        header = ctk.CTkLabel(header_frame, text="Profile", font=("Roboto", 24, "bold"), text_color="black")
        header.pack(side="left")

        # Profile Card
        profile_card = ctk.CTkFrame(self.left_frame, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
        profile_card.pack(fill="both", expand=True, padx=10, pady=10)

        # Profile Image Placeholder
        profile_img = ctk.CTkLabel(profile_card, text="🧑", font=("Arial", 50), fg_color="#f43f5e",
                                   text_color="white", width=80, height=80, corner_radius=40)
        profile_img.pack(pady=15)

        # Profile Name
        self.username_label = ctk.CTkLabel(profile_card, text=self.profile_data["name"], font=("Roboto", 18, "bold"), text_color="#1E293B")
        self.username_label.pack(pady=(5, 2))

        # Email
        self.email_label = ctk.CTkLabel(profile_card, text=self.profile_data["email"], font=("Roboto", 14), text_color="#64748B")
        self.email_label.pack(pady=5)

        # Organization Name
        self.org_label = ctk.CTkLabel(profile_card, text=f"Organization: {self.profile_data['organization']}", font=("Roboto", 14), text_color="#64748B")
        self.org_label.pack(pady=5)

        # Divider Line
        divider = ctk.CTkFrame(profile_card, fg_color="#E5E7EB", height=1)
        divider.pack(fill="x", padx=20, pady=10)

        # Update Profile Button
        update_btn = ctk.CTkButton(
            profile_card, text="Update Profile", font=("Roboto", 14, "bold"),
            fg_color="#f43f5e", hover_color="#e11d48", width=150, height=25, corner_radius=8, text_color="white",
            command=self.open_update_profile  # Open Update Profile Page
        )
        update_btn.pack(pady=10)

    def open_update_profile(self):
        """Clear the left section and show the Update Profile Form."""
        self.clear_left_frame()
        UpdateProfileForm(self.left_frame, self.app, self.save_updated_profile).pack(fill="both", expand=True)

    def save_updated_profile(self, updated_data):
        """Save the updated profile data and return to the Profile page."""
        self.profile_data.update(updated_data)  # Update profile info
        self.show_profile_section()  # Reload profile page with updated info

    def clear_left_frame(self):
        """Clear all widgets in the left frame."""
        for widget in self.left_frame.winfo_children():
            widget.destroy()

