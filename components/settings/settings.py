# import customtkinter as ctk
# import json
# import os


# class SettingsSection(ctk.CTkFrame):
#     def __init__(self, parent, app):
#         super().__init__(parent)
#         self.app = app
#         self.configure(fg_color="white")  # Default to Light Mode

#         # Store Theme Selection
#         self.theme_file = "theme.json"
#         self.current_theme = self.load_theme()

#         # Left Section (Settings)
#         self.left_frame = ctk.CTkFrame(self, corner_radius=0)
#         self.left_frame.pack(fill="both", expand=True, padx=0, pady=0)
#         self.left_frame.pack_propagate(False)

#         # Apply Theme
#         self.apply_theme()

#         # Create Settings Section
#         self._create_settings_section()

#     def _create_settings_section(self):
#         """Create a well-structured settings panel."""
#         header = ctk.CTkLabel(self.left_frame, text="Settings", font=("Roboto", 24, "bold"), text_color=self.text_color)
#         header.pack(pady=15)

#         theme_label = ctk.CTkLabel(self.left_frame, text="Select Theme", font=("Roboto", 16), text_color=self.text_color)
#         theme_label.pack(anchor="w", padx=20, pady=10)

#         self.theme_option_menu = ctk.CTkOptionMenu(
#             self.left_frame,
#             values=["Light", "Dark"],
#             width=320,
#             height=40,
#             fg_color=self.button_color,
#             text_color=self.button_text_color,
#             dropdown_fg_color=self.dropdown_color,
#             dropdown_hover_color=self.dropdown_hover,
#             button_color=self.primary_color,
#             button_hover_color=self.button_hover,
#             command=self.change_theme
#         )
#         self.theme_option_menu.set(self.current_theme)  # Set default theme
#         self.theme_option_menu.pack(anchor="w", padx=20, pady=10)

#         # Save Button
#         save_btn = ctk.CTkButton(
#             self.left_frame,
#             text="Save Settings",
#             font=("Roboto", 14, "bold"),
#             fg_color=self.primary_color,
#             hover_color=self.button_hover,
#             text_color="white",
#             width=180,
#             height=40,
#             corner_radius=8,
#             command=self.save_settings
#         )
#         save_btn.pack(pady=15)

#     def change_theme(self, theme):
#         """Apply the selected theme dynamically."""
#         self.current_theme = theme
#         self.apply_theme()

#     def apply_theme(self):
#         """Change colors and apply the selected theme."""
#         if self.current_theme == "Dark":
#             # Dark Mode Colors
#             self.bg_color = "#1E1E1E"  # Dark Gray Background
#             self.text_color = "#F8F9FA"  # Light Gray Text
#             self.button_color = "#2D2D2D"  # Dark Button
#             self.button_text_color = "#F8F9FA"
#             self.button_hover = "#444444"  # Lighter Dark Button Hover
#             self.primary_color = "#BB86FC"  # Purple Accent
#             self.dropdown_color = "#333333"
#             self.dropdown_hover = "#444444"
#         else:
#             # Light Mode Colors (Default)
#             self.bg_color = "white"
#             self.text_color = "#1E293B"
#             self.button_color = "white"
#             self.button_text_color = "black"
#             self.button_hover = "#E2E8F0"
#             self.primary_color = "#f43f5e"  # Red Accent
#             self.dropdown_color = "white"
#             self.dropdown_hover = "#f2f4f7"

#         # Apply theme to UI
#         self.configure(fg_color=self.bg_color)
#         self.left_frame.configure(fg_color=self.bg_color)

#     def save_settings(self):
#         """Save the selected theme in a JSON file."""
#         with open(self.theme_file, "w") as f:
#             json.dump({"theme": self.current_theme}, f)
#         print(f"Settings saved! Selected theme: {self.current_theme}")

#     def load_theme(self):
#         """Load the saved theme from a JSON file."""
#         if os.path.exists(self.theme_file):
#             with open(self.theme_file, "r") as f:
#                 data = json.load(f)
#                 return data.get("theme", "Light")
#         return "Light"  # Default to Light Mode




import customtkinter as ctk
import json
import os

class SettingsSection(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(fg_color="white")  # Default to Light Mode

        # Store Theme Selection
        self.theme_file = "theme.json"
        self.current_theme = self.load_theme()

        # Left Section (Settings)
        self.left_frame = ctk.CTkFrame(self, corner_radius=0)
        self.left_frame.pack(fill="both", expand=True, padx=0, pady=0)
        self.left_frame.pack_propagate(False)

        # Apply Theme
        self.apply_theme()

        # Create Settings Section
        self._create_settings_section()

    def _create_settings_section(self):
        """Create a well-structured settings panel."""
        header = ctk.CTkLabel(self.left_frame, text="Settings", font=("Roboto", 24, "bold"), text_color=self.text_color)
        header.pack(pady=15)

        theme_label = ctk.CTkLabel(self.left_frame, text="Select Theme", font=("Roboto", 16), text_color=self.text_color)
        theme_label.pack(anchor="w", padx=20, pady=10)

        self.theme_option_menu = ctk.CTkOptionMenu(
            self.left_frame,
            values=["Light", "Dark"],
            width=320,
            height=40,
            fg_color=self.button_color,
            text_color=self.button_text_color,
            dropdown_fg_color=self.dropdown_color,
            dropdown_hover_color=self.dropdown_hover,
            button_color=self.primary_color,
            button_hover_color=self.button_hover
        )
        self.theme_option_menu.set(self.current_theme)  # Set default theme
        self.theme_option_menu.pack(anchor="w", padx=20, pady=10)

        # Save Button
        save_btn = ctk.CTkButton(
            self.left_frame,
            text="Save Settings",
            font=("Roboto", 14, "bold"),
            fg_color=self.primary_color,
            hover_color=self.button_hover,
            text_color="white",
            width=180,
            height=40,
            corner_radius=8,
            command=self.save_settings
        )
        save_btn.pack(pady=15)

    def apply_theme(self):
        """Change colors and apply the selected theme."""
        if self.current_theme == "Dark":
            # Dark Mode Colors
            self.bg_color = "#1E1E1E"  # Dark Gray Background
            self.text_color = "#F8F9FA"  # Light Gray Text
            self.button_color = "#2D2D2D"  # Dark Button
            self.button_text_color = "#F8F9FA"
            self.button_hover = "#444444"  # Lighter Dark Button Hover
            self.primary_color = "#BB86FC"  # Purple Accent
            self.dropdown_color = "#333333"
            self.dropdown_hover = "#444444"
        else:
            # Light Mode Colors (Default)
            self.bg_color = "white"
            self.text_color = "#1E293B"
            self.button_color = "white"
            self.button_text_color = "black"
            self.button_hover = "#E2E8F0"
            self.primary_color = "#f43f5e"  # Red Accent
            self.dropdown_color = "white"
            self.dropdown_hover = "#f2f4f7"

        # Apply theme to UI
        self.configure(fg_color=self.bg_color)
        self.left_frame.configure(fg_color=self.bg_color)

    def save_settings(self):
        """Save the selected theme and apply it globally."""
        with open(self.theme_file, "w") as f:
            json.dump({"theme": self.theme_option_menu.get()}, f)

        # Apply theme across the entire application
        self.app.current_theme = self.theme_option_menu.get()
        self.app.apply_theme()  # Call global theme update
        print(f"Settings saved! Selected theme: {self.current_theme}")

    def load_theme(self):
        """Load the saved theme from a JSON file."""
        if os.path.exists(self.theme_file):
            with open(self.theme_file, "r") as f:
                data = json.load(f)
                return data.get("theme", "Light")
        return "Light"  # Default to Light Mode
