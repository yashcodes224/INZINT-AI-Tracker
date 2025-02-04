import customtkinter as ctk
import threading
import time
import random
from utils.aws_uploader import AWSScreenshotUploaderMongoDB

class TimerMixin:
    def __init__(self, app):
        self.timer_running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.uploader = AWSScreenshotUploaderMongoDB()
        self.app = app
        self.playing = False

    def create_timer_section(self, parent):
        """Create a professional timer UI"""

        # Section Header
        task_label = ctk.CTkLabel(parent, text="What are you working on?",
                                  font=("Roboto", 16, "bold"), text_color="#1E293B")
        task_label.pack(anchor="w", padx=20, pady=(15, 8))

        # Dropdowns Section
        self.project_option_menu = self.create_dropdown(parent,
                                                        ["Inhouse AI Tracker", "Project X", "Other"])
        self.project_option_menu.pack(anchor="w", padx=20, pady=5)

        self.sub_project_option_menu = self.create_dropdown(parent,
                                                            ["iTrack Desktop UI", "Backend Service", "Other"])
        self.sub_project_option_menu.pack(anchor="w", padx=20, pady=(5, 20))

        # Timer Container (Main Box)
        timer_container = ctk.CTkFrame(parent, fg_color="white", corner_radius=12,
                                       border_width=2, border_color="#E5E7EB")
        timer_container.pack(padx=0, pady=0)

        # Timer & Play Button Row
        timer_row = ctk.CTkFrame(timer_container, fg_color="transparent")
        timer_row.pack(pady=15, padx=15, fill="x", ipadx=10, ipady=20)

        # Timer Display (Hours:Minutes)
        self.timer_display = ctk.CTkLabel(timer_row, text="00:00",
                                          font=("Roboto", 42, "bold"), text_color="#1E293B")
        self.timer_display.pack(side="left", padx=(30, 5))  # Centered in the row

        # Small seconds timer (Smaller Size)
        self.timer_seconds = ctk.CTkLabel(timer_row, text="00",
                                          font=("Roboto", 18), text_color="#64748B")
        self.timer_seconds.pack(side="left", pady=20)

        # Play/Stop Button (Parallel to Timer)
        self.play_button = ctk.CTkButton(timer_row, text="▶",
                                          font=("Roboto", 18, "bold"), width=55, height=55,
                                          fg_color="#10B981", text_color="white",
                                          hover_color="#059669", corner_radius=28,
                                          command=self.toggle_timer)
        self.play_button.pack(side="right", padx=(20, 30))  # Aligned to right

        # Stats Section
        self.create_stats_section(parent)

        # Bottom Sync Status
        bottom_status = ctk.CTkLabel(parent, text="Last updated at 09:18 AM 🔄 Sync",
                                     font=("Roboto", 12), text_color="#64748B")
        bottom_status.pack(side="bottom", pady=15)

        # Start Timer Update
        self.update_timer_display()

    def create_dropdown(self, parent, values):
        """Create a professional dropdown menu."""
        return ctk.CTkOptionMenu(parent, values=values, width=340, height=42,
                                 fg_color="white", text_color="black",
                                 dropdown_fg_color="white", dropdown_hover_color="#f2f4f7",
                                 button_color="#f43f5e", button_hover_color="#e11d48")

    def create_stats_section(self, parent):
        """Create the stats section for Today and This Week."""
        stats_container = ctk.CTkFrame(parent, fg_color="white", corner_radius=12,
                                       border_width=1, border_color="#E5E7EB")
        stats_container.pack(fill="x", padx=20, pady=40)

        # Today’s Stats
        self.create_stat_row(stats_container, "Today", "00h 19m", "98%")

        # This Week’s Stats
        self.create_stat_row(stats_container, "This Week", "00h 19m", "98%", bottom_spacing=True)

    def create_stat_row(self, parent, label, time, percentage, bottom_spacing=False):
        """Create a single row in the stats section."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=(8, 15) if bottom_spacing else 8)

        ctk.CTkLabel(frame, text=label, font=("Roboto", 14), text_color="#1E293B").pack(side="left")
        ctk.CTkLabel(frame, text=time, font=("Roboto", 14, "bold"), text_color="#1E293B").pack(side="left", padx=10)
        ctk.CTkLabel(frame, text=percentage, font=("Roboto", 14, "bold"), text_color="#10B981").pack(side="right")

    def toggle_timer(self):
        """Toggle between start and stop."""
        if self.timer_running:
            self.stop_timer()
        else:
            self.start_timer()

    def start_timer(self):
        """Start the timer and change button appearance."""
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time() - self.elapsed_time
            self.uploader.capture_and_upload_screenshot(action="start")
            threading.Thread(target=self.capture_random_screenshots, daemon=True).start()

            # Change button to Stop mode
            self.play_button.configure(text="■", fg_color="#f43f5e", hover_color="#e11d48")

    def stop_timer(self):
        """Stop the timer and revert button appearance."""
        if self.timer_running:
            self.timer_running = False
            self.elapsed_time = time.time() - self.start_time
            self.uploader.capture_and_upload_screenshot(action="stop")

            # Change button to Play mode
            self.play_button.configure(text="▶", fg_color="#10B981", hover_color="#059669")

    def update_timer(self):
        """Update the timer's elapsed time."""
        if self.timer_running:
            self.elapsed_time = time.time() - self.start_time
        hours, minutes, seconds = self.format_time(self.elapsed_time)
        return f"{hours}:{minutes}", seconds  # Returns formatted time as HH:MM and small SS separately

    def update_timer_display(self):
        """Update the timer display label every second."""
        if hasattr(self, "timer_display"):
            formatted_time, seconds = self.update_timer()
            self.timer_display.configure(text=formatted_time)
            self.timer_seconds.configure(text=seconds)
            self.timer_display.after(1000, self.update_timer_display)

    def capture_random_screenshots(self):
        """Capture random screenshots while the timer is running."""
        while self.timer_running:
            intervals = sorted(random.sample(range(1, 600), 5))
            for interval in intervals:
                time.sleep(interval)
                if not self.timer_running:
                    return
                self.uploader.capture_and_upload_screenshot(action="random")

    @staticmethod
    def format_time(seconds):
        """Convert seconds into HH:MM:SS format, ensuring leading zeroes."""
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}", f"{minutes:02}", f"{seconds:02}"  # Ensures leading zeroes