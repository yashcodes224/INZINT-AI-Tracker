import tkinter as tk
from tkinter import ttk
import time
import threading
import random
from aws_uploader import AWSScreenshotUploaderMongoDB  # Ensure this is implemented properly


# TrackerApp class
class TrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Tracker")
        self.geometry("1000x600")
        self.configure(bg="#1e293b")

        # Sidebar
        self.create_sidebar()

        # Main content
        self.content_frame = tk.Frame(self, bg="#1e293b")
        self.content_frame.pack(side="left", fill="both", expand=True)

        # Load the TaskPage initially
        self.show_tasks()

    def create_sidebar(self):
        sidebar = tk.Frame(self, bg="#334155", width=100)
        sidebar.pack(side="left", fill="y")

        # Sidebar buttons
        buttons = [
            ("Profile", self.show_profile),
            ("Tasks", self.show_tasks),
            ("Settings", self.show_settings),
        ]
        for btn_name, command in buttons:
            btn = tk.Button(
                sidebar,
                text=btn_name,
                bg="#334155",
                fg="white",
                activebackground="#475569",
                relief="flat",
                font=("Arial", 12),
                height=2,
                width=12,
                command=command,
            )
            btn.pack(pady=10)

    def clear_content(self):
        """Clear the main content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_profile(self):
        self.clear_content()
        ProfilePage(self.content_frame, self).pack(fill="both", expand=True)

    def show_tasks(self):
        self.clear_content()
        TaskPage(self.content_frame, self).pack(fill="both", expand=True)

    def show_settings(self):
        self.clear_content()
        SettingsPage(self.content_frame, self).pack(fill="both", expand=True)


class TimerMixin:
    """Mixin class for adding timer functionality to different pages."""

    def create_timer_section(self, parent):
        """Creates the timer section in the right frame."""
        header = tk.Label(
            parent,
            text="Timer",
            font=("Arial", 16, "bold"),
            bg="#334155",
            fg="white",
        )
        header.pack(anchor="w", padx=10, pady=10)

        # Timer display
        self.timer_running = False
        self.elapsed_time = 0
        self.start_time = 0
        self.timer_text = "00:00:00"
        self.screenshot_thread = None

        self.timer_display = tk.Label(
            parent,
            text=self.timer_text,
            font=("Arial", 20, "bold"),
            bg="#334155",
            fg="#3b82f6",
        )
        self.timer_display.pack(anchor="w", padx=10)

        # Timer controls
        controls_frame = tk.Frame(parent, bg="#334155")
        controls_frame.pack(anchor="w", padx=10, pady=10)

        play_button = tk.Button(
            controls_frame,
            text="▶",
            font=("Arial", 15),
            bg="#10b981",
            fg="white",
            relief="flat",
            width=5,
            command=self.toggle_timer,
        )
        play_button.pack(side="left", padx=5)

        stop_button = tk.Button(
            controls_frame,
            text="■",
            font=("Arial", 15),
            bg="#ef4444",
            fg="white",
            relief="flat",
            width=5,
            command=self.stop_timer,
        )
        stop_button.pack(side="left", padx=5)

        # Initialize the AWS uploader
        self.uploader = AWSScreenshotUploaderMongoDB()

    def toggle_timer(self):
        if self.timer_running:
            self.stop_timer()
        else:
            self.start_timer()

    def start_timer(self):
        """Start the timer, capture screenshot, and upload to AWS."""
        self.timer_running = True
        self.start_time = time.time() - self.elapsed_time
        self.uploader.capture_and_upload_screenshot(action="start")
        self.update_timer()

        # Start a separate thread for random screenshots
        self.screenshot_thread = threading.Thread(target=self.capture_random_screenshots, daemon=True)
        self.screenshot_thread.start()

    def stop_timer(self):
        """Stop the timer, capture screenshot, and upload to AWS."""
        self.timer_running = False
        self.elapsed_time = time.time() - self.start_time
        self.timer_display.config(text=self.format_time(self.elapsed_time))
        self.uploader.capture_and_upload_screenshot(action="stop")

    def update_timer(self):
        if self.timer_running:
            self.elapsed_time = time.time() - self.start_time
            self.timer_display.config(text=self.format_time(self.elapsed_time))
            self.after(100, self.update_timer)


    def capture_random_screenshots(self):
        """Capture random screenshots within each 10-minute period."""
        while self.timer_running:
            # Capture 5 random screenshots in a 10-minute period
            start_time = time.time()
            intervals = sorted(random.sample(range(1, 600), 5))  # Random seconds within 10 minutes
            for interval in intervals:
                if not self.timer_running:
                    return  # Stop if the timer has stopped
                sleep_time = interval - (time.time() - start_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                if not self.timer_running:
                    return  # Check again after sleeping
                self.uploader.capture_and_upload_screenshot(action="random")

            # Ensure the loop doesn't start before the 10-minute window ends
            elapsed = time.time() - start_time
            time.sleep(max(0, 600 - elapsed))

    @staticmethod
    def format_time(seconds):
        """Format time in HH:MM:SS format."""
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"


class TaskPage(tk.Frame, TimerMixin):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.configure(bg="#1e293b")
        self.app = app

        # Main content split into two sections: left and right
        self.left_frame = tk.Frame(self, bg="#1e293b")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.right_frame = tk.Frame(self, bg="#334155", width=250)
        self.right_frame.pack(side="right", fill="y")

        # Left Section
        self.create_task_section()

        # Right Section (Timer and stats)
        self.create_timer_section(self.right_frame)

    def create_task_section(self):
        header = tk.Label(
            self.left_frame,
            text="My Tasks",
            font=("Arial", 16, "bold"),
            bg="#1e293b",
            fg="white",
        )
        header.pack(anchor="w", pady=10)

        # Task list
        tasks = [("ICRM", "desktop-app"), ("ICRM", "testing")]
        for project, task in tasks:
            task_frame = tk.Frame(self.left_frame, bg="#334155", padx=10, pady=5)
            task_frame.pack(fill="x", pady=5)

            project_label = tk.Label(
                task_frame, text=project, font=("Arial", 12), bg="#334155", fg="white"
            )
            project_label.pack(side="left", padx=5)

            task_label = tk.Label(
                task_frame,
                text=task,
                font=("Arial", 10),
                bg="#334155",
                fg="#cbd5e1",
            )
            task_label.pack(side="left", padx=10)


class ProfilePage(tk.Frame, TimerMixin):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.configure(bg="#1e293b")
        self.app = app

        # Main content split into two sections: left and right
        self.left_frame = tk.Frame(self, bg="#1e293b")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.right_frame = tk.Frame(self, bg="#334155", width=250)
        self.right_frame.pack(side="right", fill="y")

        # Left Section
        tk.Label(
            self.left_frame,
            text="Profile Information",
            font=("Arial", 16, "bold"),
            bg="#1e293b",
            fg="white",
        ).pack(anchor="w", pady=10)

        # Right Section (Timer and stats)
        self.create_timer_section(self.right_frame)


class SettingsPage(tk.Frame, TimerMixin):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.configure(bg="#1e293b")
        self.app = app

        # Main content split into two sections: left and right
        self.left_frame = tk.Frame(self, bg="#1e293b")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.right_frame = tk.Frame(self, bg="#334155", width=250)
        self.right_frame.pack(side="right", fill="y")

        # Left Section
        tk.Label(
            self.left_frame,
            text="Settings",
            font=("Arial", 16, "bold"),
            bg="#1e293b",
            fg="white",
        ).pack(anchor="w", pady=10)

        # Right Section (Timer and stats)
        self.create_timer_section(self.right_frame)


if __name__ == "__main__":
    app = TrackerApp()
    app.mainloop()
