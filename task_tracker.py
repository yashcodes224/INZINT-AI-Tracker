import customtkinter as ctk
import time
import threading
import random
from PIL import Image
import os
from customtkinter import CTkImage
from aws_uploader import AWSScreenshotUploaderMongoDB  # Ensure this is implemented properly

# Define theme colors
PRIMARY_COLOR = "#0f172a"
SECONDARY_COLOR = "#1e293b"
HIGHLIGHT_COLOR = "#3b82f6"
TEXT_COLOR = "white"
SIDEBAR_BG_COLOR = "#334155"
BUTTON_BG_COLOR = "#475569"
BUTTON_HOVER_COLOR = "#3b82f6"


class TrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Task Tracker")
        self.geometry("1000x600")
        self.configure(fg_color=PRIMARY_COLOR)

        # Timer state
        self.timer_running = False
        self.elapsed_time = 0
        self.start_time = 0
        self.screenshot_thread = None
        self.uploader = AWSScreenshotUploaderMongoDB()

        # Sidebar
        self.create_sidebar()

        # Main content
        self.content_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR)
        self.content_frame.pack(side="left", fill="both", expand=True)

        # Load the TaskPage initially
        self.show_tasks()

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color=SIDEBAR_BG_COLOR, width=150, corner_radius=0)
        sidebar.pack(side="left", fill="y")

        # Profile image with CTkImage
        image = Image.open("user.png").resize((100, 100))
        profile_image = CTkImage(light_image=image, size=(100, 100))
        profile_label = ctk.CTkLabel(sidebar, image=profile_image, text="")
        profile_label.pack(pady=20)

        # Sidebar buttons
        buttons = [
            ("Profile", self.show_profile),
            ("Tasks", self.show_tasks),
            ("Settings", self.show_settings),
        ]
        for btn_name, command in buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=btn_name,
                fg_color=BUTTON_BG_COLOR,
                text_color=TEXT_COLOR,
                hover_color=BUTTON_HOVER_COLOR,
                font=("Roboto", 14),
                command=command,
                corner_radius=10,
                width=120
            )
            btn.pack(pady=10)
        # Add Sign Out Button at the Bottom
        sign_out_button = ctk.CTkButton(
            sidebar,
            text="Sign Out",
            fg_color="#ef4444",
            text_color=TEXT_COLOR,
            hover_color="#dc2626",
            font=("Roboto", 14),
            command=self.sign_out,
            corner_radius=10,
            width=120
        )
        sign_out_button.pack(side="bottom", pady=20)

    def clear_content(self):
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

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time() - self.elapsed_time
            self.uploader.capture_and_upload_screenshot(action="start")
            threading.Thread(target=self.capture_random_screenshots, daemon=True).start()

    def stop_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.elapsed_time = time.time() - self.start_time
            self.uploader.capture_and_upload_screenshot(action="stop")

    def update_timer(self):
        if self.timer_running:
            self.elapsed_time = time.time() - self.start_time
            return self.format_time(self.elapsed_time)
        return self.format_time(self.elapsed_time)

    def capture_random_screenshots(self):
        while self.timer_running:
            intervals = sorted(random.sample(range(1, 600), 5))
            for interval in intervals:
                time.sleep(interval)
                if not self.timer_running:
                    return
                self.uploader.capture_and_upload_screenshot(action="random")
    def sign_out(self):
        """Handles the sign-out process and returns to final.py."""
        self.destroy()  # Close the current application window
        os.system("python final.py")  # Execute the final.py script
    @staticmethod
    def format_time(seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"


class TimerMixin:
    def create_timer_section(self, parent):
        header = ctk.CTkLabel(
            parent,
            text="Timer",
            font=("Roboto", 16, "bold"),
            text_color=TEXT_COLOR,
        )
        header.pack(anchor="w", padx=10, pady=10)

        self.timer_display = ctk.CTkLabel(
            parent,
            text=self.app.update_timer(),
            font=("Roboto", 24, "bold"),
            text_color=HIGHLIGHT_COLOR,
        )
        self.timer_display.pack(anchor="w", padx=10)

        controls_frame = ctk.CTkFrame(parent, fg_color=SECONDARY_COLOR)
        controls_frame.pack(anchor="w", padx=10, pady=10)

        play_button = ctk.CTkButton(
            controls_frame,
            text="▶",
            font=("Roboto", 14),
            fg_color="#10b981",
            text_color=TEXT_COLOR,
            hover_color="#059669",
            width=50,
            command=self.app.start_timer,
        )
        play_button.pack(side="left", padx=5)

        stop_button = ctk.CTkButton(
            controls_frame,
            text="■",
            font=("Roboto", 14),
            fg_color="#ef4444",
            text_color=TEXT_COLOR,
            hover_color="#dc2626",
            width=50,
            command=self.app.stop_timer,
        )
        stop_button.pack(side="left", padx=5)

        self.update_timer_display()

    def update_timer_display(self):
        self.timer_display.configure(text=self.app.update_timer())
        self.after(1000, self.update_timer_display)


class TaskPage(ctk.CTkFrame, TimerMixin):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.configure(fg_color=PRIMARY_COLOR)
        self.app = app

        self.left_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.right_frame = ctk.CTkFrame(self, fg_color=SECONDARY_COLOR, width=250)
        self.right_frame.pack(side="right", fill="y")

        self.create_task_section()
        self.create_timer_section(self.right_frame)

    def create_task_section(self):
        header = ctk.CTkLabel(
            self.left_frame,
            text="Tasks",
            font=("Roboto", 16, "bold"),
            text_color=TEXT_COLOR,
        )
        header.pack(anchor="w", pady=10)

        tasks = [("ICRM", "desktop-app"), ("ICRM", "testing")]
        for project, task in tasks:
            task_frame = ctk.CTkFrame(self.left_frame, fg_color=SIDEBAR_BG_COLOR, corner_radius=10)
            task_frame.pack(fill="x", pady=5, padx=10)

            project_label = ctk.CTkLabel(
                task_frame, text=project, font=("Roboto", 14), text_color=TEXT_COLOR
            )
            project_label.pack(side="left", padx=5)

            task_label = ctk.CTkLabel(
                task_frame,
                text=task,
                font=("Roboto", 16),
                text_color="#cbd5e1",
            )
            task_label.pack(side="left", padx=10)


class ProfilePage(ctk.CTkFrame, TimerMixin):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.configure(fg_color=PRIMARY_COLOR)
        self.app = app

        self.left_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.right_frame = ctk.CTkFrame(self, fg_color=SECONDARY_COLOR, width=250)
        self.right_frame.pack(side="right", fill="y")

        ctk.CTkLabel(
            self.left_frame,
            text="User's Profile",
            font=("Roboto", 16, "bold"),
            text_color=TEXT_COLOR,
        ).pack(anchor="w", pady=10)

        self.create_timer_section(self.right_frame)


class SettingsPage(ctk.CTkFrame, TimerMixin):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.configure(fg_color=PRIMARY_COLOR)
        self.app = app

        self.left_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.right_frame = ctk.CTkFrame(self, fg_color=SECONDARY_COLOR, width=250)
        self.right_frame.pack(side="right", fill="y")

        ctk.CTkLabel(
            self.left_frame,
            text="Settings",
            font=("Roboto", 16, "bold"),
            text_color=TEXT_COLOR,
        ).pack(anchor="w", pady=10)

        self.create_timer_section(self.right_frame)

if __name__ == "__main__":
    app = TrackerApp()
    app.mainloop()
