import customtkinter as ctk
from components.settings.settings_style import LIGHT_THEME, DARK_THEME  

class SettingsSection(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app  # Store reference to main app

        # Use app's theme (default is Light Mode)
        self.current_theme = self.app.current_theme  

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
        header = ctk.CTkLabel(
            self.left_frame, 
            text="Settings", 
            font=self.theme["header"]["font"], 
            text_color=self.theme["header"]["text_color"]
        )
        header.pack(pady=15)

        theme_label = ctk.CTkLabel(
            self.left_frame, 
            text="Select Theme", 
            font=self.theme["label"]["font"], 
            text_color=self.theme["label"]["text_color"]
        )
        theme_label.pack(anchor="w", padx=20, pady=10)

        self.theme_option_menu = ctk.CTkOptionMenu(
            self.left_frame,
            values=["Light", "Dark"],
            width=320, height=40,
            fg_color=self.theme["theme_option_menu"]["fg_color"],
            text_color=self.theme["theme_option_menu"]["text_color"],
            dropdown_fg_color=self.theme["theme_option_menu"]["dropdown_fg_color"],
            dropdown_hover_color=self.theme["theme_option_menu"]["dropdown_hover_color"],
            button_color=self.theme["theme_option_menu"]["button_color"],
            button_hover_color=self.theme["theme_option_menu"]["button_hover_color"],
            dropdown_text_color=self.theme["theme_option_menu"]["dropdown_text_color"]
        )
        self.theme_option_menu.set(self.current_theme)  # Set current theme
        self.theme_option_menu.pack(anchor="w", padx=20, pady=10)

        # Save Button
        save_btn = ctk.CTkButton(
            self.left_frame,
            text="Save Settings",
            width=180, height=40,
            corner_radius=8,
            fg_color=self.theme["save_button"]["fg_color"],
            text_color="white",
            hover_color=self.theme["save_button"]["hover_color"],
            command=self.save_settings
        )
        save_btn.pack(pady=15)

    def apply_theme(self):
        """Apply the selected theme to the settings UI."""
        self.theme = LIGHT_THEME if self.current_theme == "Light" else DARK_THEME

        # Apply theme to UI elements
        self.configure(fg_color=self.theme["default_bg_color"])
        self.left_frame.configure(fg_color=self.theme["default_bg_color"])

    def save_settings(self):
        """Apply the selected theme instantly without restarting the app."""
        selected_theme = self.theme_option_menu.get()

        # Set the theme in the main app and update the UI
        self.app.set_theme(selected_theme)  
        print(f"Settings saved! Selected theme: {selected_theme}")
