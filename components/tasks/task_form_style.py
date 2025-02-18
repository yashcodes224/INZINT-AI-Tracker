# task_form_style.py

LIGHT_THEME = {
    "background": "#f2f4f7",
    
    "header": {
        "font": ("Roboto", 22, "bold"),
        "text_color": "#1E293B",
    },

    "label": {
        "font": ("Roboto", 14),
        "text_color": "#1E293B",
    },

    "entry": {
        "width": 320,
        "height": 40,
        "fg_color": "white",
        "text_color": "black",
        "border_width": 2,
        "border_color": "#D1D5DB",
        "focus_border_color": "#f43f5e",
    },

    "dropdown": {
        "values": ["Inhouse AI Tracker", "Project X", "Other"],
        "width": 320,
        "height": 40,
        "fg_color": "white",
        "text_color": "black",
        "dropdown_fg_color": "white",
        "dropdown_hover_color": "#f2f4f7",
        "button_color": "#f43f5e",
        "button_hover_color": "#e11d48",
        "focus_button_color": "#f43f5e",
        "dropdown_text_color": "black"
    },

    "cancel_button": {
        "width": 150,
        "height": 40,
        "fg_color": "white",
        "text_color": "black",
        "border_width": 1,
        "border_color": "#D1D5DB",
        "hover_color": "#E2E8F0",
        "font": ("Roboto", 14, "bold"),
        "corner_radius": 8,
    },

    "create_button": {
        "width": 150,
        "height": 40,
        "fg_color": "#f43f5e",
        "text_color": "white",
        "hover_color": "#e11d48",
        "font": ("Roboto", 14, "bold"),
        "corner_radius": 8,
    },
}

DARK_THEME = {
    "background": "#121212",  # Dark Gray
    
    "header": {
        "font": ("Roboto", 22, "bold"),
        "text_color": "#F8F9FA",
    },

    "label": {
        "font": ("Roboto", 14),
        "text_color": "#F8F9FA",
    },

    "entry": {
        "width": 320,
        "height": 40,
        "fg_color": "#1E1E1E",  # Darker Input Field
        "text_color": "white",
        "border_width": 2,
        "border_color": "#444444",
        "focus_border_color": "#BB86FC",  # Purple Focus
    },

    "dropdown": {
        "values": ["Inhouse AI Tracker", "Project X", "Other"],
        "width": 320,
        "height": 40,
        "fg_color": "#1E1E1E",
        "text_color": "white",
        "dropdown_fg_color": "#2A2A2A",
        "dropdown_hover_color": "#333333",
        "button_color": "#BB86FC",
        "button_hover_color": "#9E68E2",
        "focus_button_color": "#BB86FC",
        "dropdown_text_color": "white"
    },

    "cancel_button": {
        "width": 150,
        "height": 40,
        "fg_color": "#333333",
        "text_color": "white",
        "border_width": 1,
        "border_color": "#444444",
        "hover_color": "#555555",
        "font": ("Roboto", 14, "bold"),
        "corner_radius": 8,
    },

    "create_button": {
        "width": 150,
        "height": 40,
        "fg_color": "#BB86FC",
        "text_color": "white",
        "hover_color": "#9E68E2",
        "font": ("Roboto", 14, "bold"),
        "corner_radius": 8,
    },
}
