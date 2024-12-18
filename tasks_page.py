import tkinter as tk
from tkinter import ttk


class TasksPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg="#1e293b")

        # Header
        header = tk.Label(self, text="My Tasks", font=("Arial", 16, "bold"),
                          bg="#1e293b", fg="white")
        header.pack(anchor="w", pady=10)

        # Task List
        task_list = tk.Frame(self, bg="#1e293b")
        task_list.pack(fill="both", expand=True)

        tasks = [("desktop-app", "ICRM"), ("testing", "ICRM")]
        for task_name, project in tasks:
            task_frame = tk.Frame(task_list, bg="#334155", padx=10, pady=5)
            task_frame.pack(fill="x", pady=5)

            task_label = tk.Label(task_frame, text=task_name, font=("Arial", 12),
                                  bg="#334155", fg="white")
            task_label.pack(side="left", padx=5)

            project_label = tk.Label(task_frame, text=project, font=("Arial", 10),
                                     bg="#334155", fg="#cbd5e1")
            project_label.pack(side="left", padx=10)

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
