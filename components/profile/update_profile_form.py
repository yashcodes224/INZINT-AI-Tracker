import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


class UpdateProfileForm(ctk.CTkFrame):
    def __init__(self, parent, app, on_profile_updated):
        super().__init__(parent)

        self.app = app
        self.on_profile_updated = on_profile_updated  # Callback when profile is updated

        self.configure(fg_color="#f2f4f7", corner_radius=0)  # Matching task form background

        # Header
        header = ctk.CTkLabel(self, text="Update Profile", font=("Roboto", 22, "bold"), text_color="#1E293B")
        header.pack(anchor="w", padx=20, pady=(20, 15))

        # Name Field
        name_label = ctk.CTkLabel(self, text="Full Name *", font=("Roboto", 14), text_color="#1E293B")
        name_label.pack(anchor="w", padx=20, pady=(10, 0))

        self.name_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter full name...",
            width=320,
            height=40,
            fg_color="white",
            text_color="black",
            border_width=2,
            border_color="#D1D5DB"
        )
        self.name_entry.pack(anchor="w", padx=20, pady=(5, 15))
        self.name_entry.bind("<FocusIn>", self.highlight_name_entry)
        self.name_entry.bind("<FocusOut>", self.reset_name_border)

        # Email Field
        email_label = ctk.CTkLabel(self, text="Email *", font=("Roboto", 14), text_color="#1E293B")
        email_label.pack(anchor="w", padx=20, pady=(10, 0))

        self.email_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter email...",
            width=320,
            height=40,
            fg_color="white",
            text_color="black",
            border_width=2,
            border_color="#D1D5DB"
        )
        self.email_entry.pack(anchor="w", padx=20, pady=(5, 15))
        self.email_entry.bind("<FocusIn>", self.highlight_email_entry)
        self.email_entry.bind("<FocusOut>", self.reset_email_border)

        # Organization Field
        org_label = ctk.CTkLabel(self, text="Organization *", font=("Roboto", 14), text_color="#1E293B")
        org_label.pack(anchor="w", padx=20, pady=(10, 0))

        self.org_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter organization name...",
            width=320,
            height=40,
            fg_color="white",
            text_color="black",
            border_width=2,
            border_color="#D1D5DB"
        )
        self.org_entry.pack(anchor="w", padx=20, pady=(5, 20))
        self.org_entry.bind("<FocusIn>", self.highlight_org_entry)
        self.org_entry.bind("<FocusOut>", self.reset_org_border)

        # Buttons Frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=30)  # Consistent spacing

        # Cancel Button
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=150,
            height=40,
            fg_color="white",
            text_color="black",
            border_width=1,
            border_color="#D1D5DB",
            hover_color="#E2E8F0",
            font=("Roboto", 14, "bold"),
            corner_radius=8,
            command=self.cancel_update
        )
        cancel_button.pack(side="left", padx=10)

        # Save Button
        save_button = ctk.CTkButton(
            button_frame,
            text="Save Changes",
            width=150,
            height=40,
            fg_color="#f43f5e",
            text_color="white",
            hover_color="#e11d48",
            font=("Roboto", 14, "bold"),
            corner_radius=8,
            command=self.save_profile
        )
        save_button.pack(side="left", padx=10)

    def highlight_name_entry(self, event):
        """Change border color to red when the entry box is clicked."""
        self.name_entry.configure(border_color="#f43f5e")

    def reset_name_border(self, event):
        """Reset border color when focus is lost."""
        self.name_entry.configure(border_color="#D1D5DB")

    def highlight_email_entry(self, event):
        """Change border color to red when the entry box is clicked."""
        self.email_entry.configure(border_color="#f43f5e")

    def reset_email_border(self, event):
        """Reset border color when focus is lost."""
        self.email_entry.configure(border_color="#D1D5DB")

    def highlight_org_entry(self, event):
        """Change border color to red when the entry box is clicked."""
        self.org_entry.configure(border_color="#f43f5e")

    def reset_org_border(self, event):
        """Reset border color when focus is lost."""
        self.org_entry.configure(border_color="#D1D5DB")

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


