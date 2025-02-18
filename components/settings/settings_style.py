# settings_style.py

LIGHT_THEME = {
    "default_bg_color": "#f2f4f7",
    "background": "#f2f4f7",  # ✅ Added this key

    "header": {
        "font": ("Roboto", 24, "bold"),
        "text_color": "#1E293B",
    },

    "label": {
        "font": ("Roboto", 16),
        "text_color": "#1E293B",
    },

    "theme_option_menu": {
        "width": 320,
        "height": 40,
        "fg_color": "white",
        "text_color": "black",
        "dropdown_fg_color": "white",
        "dropdown_hover_color": "#f2f4f7",
        "button_color": "#f43f5e",
        "button_hover_color": "#e11d48",
        "dropdown_text_color": "black"
    },

    "save_button": {
        "text": "Save Settings",
        "font": ("Roboto", 14, "bold"),
        "width": 180,
        "height": 40,
        "corner_radius": 8,
        "fg_color": "#f43f5e",
        "text_color": "white",
        "hover_color": "#e11d48",
    },
}

DARK_THEME = {
    "default_bg_color": "#1E1E1E",
    "background": "#1E1E1E",  # ✅ Added this key

    "header": {
        "font": ("Roboto", 24, "bold"),
        "text_color": "#F8F9FA",
    },

    "label": {
        "font": ("Roboto", 16),
        "text_color": "#F8F9FA",
    },

    "theme_option_menu": {
        "width": 320,
        "height": 40,
        "fg_color": "#2D2D2D",
        "text_color": "white",
        "dropdown_fg_color": "#333333",
        "dropdown_hover_color": "#2d2d2d",
        "button_color": "#BB86FC",
        "button_hover_color": "#9E68E2",
        "dropdown_text_color": "white"
    },

    "save_button": {
        "text": "Save Settings",
        "font": ("Roboto", 14, "bold"),
        "width": 180,
        "height": 40,
        "corner_radius": 8,
        "fg_color": "#BB86FC",
        "text_color": "white",
        "hover_color": "#9E68E2",
    },
}
