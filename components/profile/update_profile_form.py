import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from components.profile.update_profile_style import LIGHT_THEME, DARK_THEME  # Import styles


class UpdateProfileForm(ctk.CTkFrame):
    def __init__(self, parent, app, on_profile_updated):
        super().__init__(parent)

        self.app = app

        self.apply_theme()

        self.on_profile_updated = on_profile_updated  # Callback when profile is updated

        self.configure(fg_color=self.theme["background"])  # Set background color

        # Header
        header = ctk.CTkLabel(
            self, 
            text="Update Profile", 
            font=self.theme["header"]["font"], 
            text_color=self.theme["header"]["text_color"]
        )
        header.pack(anchor="w", padx=20, pady=(20, 15))

        # Name Field
        name_label = ctk.CTkLabel(
            self, 
            text="Full Name *", 
            font=self.theme["label"]["font"], 
            text_color=self.theme["label"]["text_color"]
        )
        name_label.pack(anchor="w", padx=20, pady=(10, 0))

        self.name_entry = ctk.CTkEntry(self, **self.theme["entry"], placeholder_text="Enter full name...")
        self.name_entry.pack(anchor="w", padx=20, pady=(5, 15))
        self.name_entry.bind("<FocusIn>", self.highlight_name_entry)
        self.name_entry.bind("<FocusOut>", self.reset_name_border)

        # Email Field
        email_label = ctk.CTkLabel(
            self, 
            text="Email *", 
            font=self.theme["label"]["font"], 
            text_color=self.theme["label"]["text_color"]
        )
        email_label.pack(anchor="w", padx=20, pady=(10, 0))

        self.email_entry = ctk.CTkEntry(self, **self.theme["entry"], placeholder_text="Enter email...")
        self.email_entry.pack(anchor="w", padx=20, pady=(5, 15))
        self.email_entry.bind("<FocusIn>", self.highlight_email_entry)
        self.email_entry.bind("<FocusOut>", self.reset_email_border)

        # Organization Field
        org_label = ctk.CTkLabel(
            self, 
            text="Organization *", 
            font=self.theme["label"]["font"], 
            text_color=self.theme["label"]["text_color"]
        )
        org_label.pack(anchor="w", padx=20, pady=(10, 0))

        self.org_entry = ctk.CTkEntry(self, **self.theme["entry"], placeholder_text="Enter organization name...")
        self.org_entry.pack(anchor="w", padx=20, pady=(5, 20))
        self.org_entry.bind("<FocusIn>", self.highlight_org_entry)
        self.org_entry.bind("<FocusOut>", self.reset_org_border)

        # Buttons Frame
        button_frame = ctk.CTkFrame(self, **self.theme["button_frame"])
        button_frame.pack(pady=30)  # Consistent spacing

        # Cancel Button
        cancel_button = ctk.CTkButton(button_frame, **self.theme["cancel_button"], command=self.cancel_update)
        cancel_button.pack(side="left", padx=10)

        # Save Button
        save_button = ctk.CTkButton(button_frame, **self.theme["save_button"], command=self.save_profile)
        save_button.pack(side="left", padx=10)

    def apply_theme(self):
        """Apply the selected theme (Light or Dark)."""
        self.theme = LIGHT_THEME if self.app.current_theme == "Light" else DARK_THEME
        self.configure(fg_color=self.theme["background"])

    def highlight_name_entry(self, event):
        """Change border color when the entry box is clicked."""
        self.name_entry.configure(border_color=self.theme["entry_focus"]["border_color"])

    def reset_name_border(self, event):
        """Reset border color when focus is lost."""
        self.name_entry.configure(border_color=self.theme["entry"]["border_color"])

    def highlight_email_entry(self, event):
        """Change border color when the entry box is clicked."""
        self.email_entry.configure(border_color=self.theme["entry_focus"]["border_color"])

    def reset_email_border(self, event):
        """Reset border color when focus is lost."""
        self.email_entry.configure(border_color=self.theme["entry"]["border_color"])

    def highlight_org_entry(self, event):
        """Change border color when the entry box is clicked."""
        self.org_entry.configure(border_color=self.theme["entry_focus"]["border_color"])

    def reset_org_border(self, event):
        """Reset border color when focus is lost."""
        self.org_entry.configure(border_color=self.theme["entry"]["border_color"])

    def cancel_update(self):
        """Return to Profile Page without saving changes."""
        self.on_profile_updated({})  # Pass empty dictionary (no updates)

    def save_profile(self):
        """Save the updated profile information and return to Profile Page."""
        updated_data = {
            "name": self.name_entry.get(),
            "email": self.email_entry.get(),
            "organization": self.org_entry.get()
        }

        # Basic validation
        if not updated_data["name"].strip() or not updated_data["email"].strip() or not updated_data["organization"].strip():
            CTkMessagebox(title="Error", message="All fields are required!", icon="cancel")
            return

        self.on_profile_updated(updated_data)  # Pass updated data back