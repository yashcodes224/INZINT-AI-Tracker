import tkinter as tk


class ProfilePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg="#1e293b")

        # Header
        header = tk.Label(self, text="Profile", font=("Arial", 16, "bold"),
                          bg="#1e293b", fg="white")
        header.pack(anchor="w", pady=10)

        # Profile Info
        profile_frame = tk.Frame(self, bg="#334155", padx=10, pady=10)
        profile_frame.pack(fill="x", pady=10)

        name_label = tk.Label(profile_frame, text="Name: Anjali Saxena", font=("Arial", 12),
                              bg="#334155", fg="white")
        name_label.pack(anchor="w", pady=5)

        email_label = tk.Label(profile_frame, text="Email: anjali@inzint.com", font=("Arial", 12),
                               bg="#334155", fg="white")
        email_label.pack(anchor="w", pady=5)

        plan_label = tk.Label(profile_frame, text="Plan: Elite", font=("Arial", 12),
                              bg="#334155", fg="white")
        plan_label.pack(anchor="w", pady=5)

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
