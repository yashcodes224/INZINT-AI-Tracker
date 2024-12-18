import tkinter as tk


class SettingsPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg="#1e293b")

        # Header
        header = tk.Label(self, text="Settings", font=("Arial", 16, "bold"),
                          bg="#1e293b", fg="white")
        header.pack(anchor="w", pady=10)

        # Preferences
        preferences_frame = tk.Frame(self, bg="#334155", padx=10, pady=10)
        preferences_frame.pack(fill="x", pady=10)

        dark_mode_label = tk.Label(preferences_frame, text="Dark Mode", font=("Arial", 12),
                                   bg="#334155", fg="white")
        dark_mode_label.pack(anchor="w", pady=5)

        # Toggle button (dummy)
        dark_mode_toggle = tk.Checkbutton(preferences_frame, text="Enable", bg="#334155",
                                          fg="white", selectcolor="#475569")
        dark_mode_toggle.pack(anchor="w", pady=5)

        # Timer section remains constant
        self.create_timer_section()

    def create_timer_section(self):
        timer_frame = tk.Frame(self, bg="#1e293b")
        timer_frame.pack(fill="x", pady=10)

        timer_label = tk.Label(timer_frame, text="00:00:00", font=("Arial", 20, "bold"),
                               bg="#1e293b", fg="#3b82f6")
        timer_label.pack(side="left", padx=10)

        play_button = tk.Button(timer_frame, text="▶", font=("Arial", 15), bg="#10b981", fg="white",
                                relief="flat", width=5)
        play_button.pack(side="left", padx=10)
