import customtkinter as ctk
import threading
import time
import random
from utils.aws_uploader import AWSScreenshotUploaderMongoDB
from components.timer.timer_style import LIGHT_THEME, DARK_THEME
import requests

class TimerMixin:
    def __init__(self, app, user_name):
        self.timer_running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.uploader = AWSScreenshotUploaderMongoDB(user_name=user_name)
        self.app = app
        self.playing = False
        self.user_name = user_name

        # Apply theme
        self.apply_theme()

    def apply_theme(self):
        """Apply selected theme."""
        self.theme = LIGHT_THEME if self.app.current_theme == "Light" else DARK_THEME

    def create_timer_section(self, parent):
        """Create a professional timer UI"""
        self.apply_theme()

        # Section Header
        self.task_label = ctk.CTkLabel(parent, text="What are you working on?",
                                  font=("Roboto", 16, "bold"), 
                                  text_color=self.theme["text_color"])
        self.task_label.pack(anchor="w", padx=20, pady=(15, 8))

        # Dropdowns Section
        self.project_option_menu = self.create_dropdown(parent, ["No Projects Assigned..."])
        self.project_option_menu.pack(anchor="w", padx=20, pady=5)

        self.sub_project_option_menu = self.create_dropdown(parent, ["iTrack Desktop UI", "Backend Service", "Other"])
        self.sub_project_option_menu.pack(anchor="w", padx=20, pady=(5, 20))

        # Timer Container
        self.timer_container = ctk.CTkFrame(parent, 
                                            fg_color=self.theme["timer_container"]["bg_color"], 
                                            corner_radius=12,
                                            border_width=2, 
                                            border_color=self.theme["timer_container"]["border_color"])
        self.timer_container.pack(padx=0, pady=0)

        # Timer Row
        timer_row = ctk.CTkFrame(self.timer_container, fg_color="transparent")
        timer_row.pack(pady=15, padx=15, fill="x", ipadx=10, ipady=20)

        # Timer Display
        self.timer_display = ctk.CTkLabel(timer_row, text="00:00",
                                          font=("Roboto", 42, "bold"), 
                                          text_color=self.theme["timer_text"]["main"])
        self.timer_display.pack(side="left", padx=(30, 5))

        # Small seconds timer
        self.timer_seconds = ctk.CTkLabel(timer_row, text="00",
                                          font=("Roboto", 18), 
                                          text_color=self.theme["timer_text"]["seconds"])
        self.timer_seconds.pack(side="left", pady=20)

        # Play/Stop Button
        self.play_button = ctk.CTkButton(timer_row, text="▶",
                                          font=("Roboto", 18, "bold"), 
                                          width=55, height=55,
                                          fg_color=self.theme["play_button"]["fg_color"], 
                                          text_color="white",
                                          hover_color=self.theme["play_button"]["hover_color"], 
                                          corner_radius=20,
                                          command=self.toggle_timer)
        self.play_button.pack(side="right", padx=(20, 30))

        # Stats Section
        self.create_stats_section(parent)

        # Bottom Sync Status
        self.bottom_status = ctk.CTkLabel(parent, text="Last updated at 09:18 AM 🔄 Sync",
                                     font=("Roboto", 12), 
                                     text_color=self.theme["subtext_color"])
        self.bottom_status.pack(side="bottom", pady=15)

        # Start Timer Update
        self.update_timer_display()

    def update_timer_theme(self):
            """Update the timer UI elements only if they exist."""
            if hasattr(self, "timer_container"):  # ✅ Check if timer UI exists
                # Update text colors for "Today" and "This Week"
                if hasattr(self, "today_label"):
                    self.today_label.configure(text_color=self.theme["text_color"])
                if hasattr(self, "today_time_label"):
                    self.today_time_label.configure(text_color=self.theme["text_color"])
                if hasattr(self, "week_label"):
                    self.week_label.configure(text_color=self.theme["text_color"])
                if hasattr(self, "week_time_label"):
                    self.week_time_label.configure(text_color=self.theme["text_color"])

                # Update other UI elements
                self.task_label.configure(text_color=self.theme["text_color"])
                self.timer_container.configure(
                    fg_color=self.theme["timer_container"]["bg_color"],
                    border_color=self.theme["timer_container"]["border_color"]
                )
                self.timer_display.configure(text_color=self.theme["text_color"])
                self.timer_seconds.configure(text_color=self.theme["text_color"])
                self.play_button.configure(
                    fg_color=self.theme["play_button"]["fg_color"],
                    hover_color=self.theme["play_button"]["hover_color"]
                )
                self.stats_container.configure(
                    fg_color=self.theme["stats_section"]["bg_color"],
                    border_color=self.theme["stats_section"]["border_color"]
                )
                self.bottom_status.configure(text_color=self.theme["text_color"])

                # ✅ Update Dropdown Colors
                self.project_option_menu.configure(
                    fg_color=self.theme["dropdown"]["fg_color"],
                    text_color=self.theme["dropdown"]["text_color"],
                    dropdown_fg_color=self.theme["dropdown"]["fg_color"],
                    dropdown_hover_color=self.theme["dropdown"]["dropdown_hover_color"],
                    button_color=self.theme["dropdown"]["button_color"],
                    button_hover_color=self.theme["dropdown"]["button_hover_color"],
                    dropdown_text_color=self.theme["dropdown"]["dropdown_text_color"]
                )

                self.sub_project_option_menu.configure(
                    fg_color=self.theme["dropdown"]["fg_color"],
                    text_color=self.theme["dropdown"]["text_color"],
                    dropdown_fg_color=self.theme["dropdown"]["fg_color"],
                    dropdown_hover_color=self.theme["dropdown"]["dropdown_hover_color"],
                    button_color=self.theme["dropdown"]["button_color"],
                    button_hover_color=self.theme["dropdown"]["button_hover_color"],
                    dropdown_text_color=self.theme["dropdown"]["dropdown_text_color"]
                )

    def create_dropdown(self, parent, values):
        """Create a dropdown menu with theme support."""
        return ctk.CTkOptionMenu(parent, values=values, width=340, height=42,
                                 fg_color=self.theme["dropdown"]["fg_color"],
                                 text_color=self.theme["dropdown"]["text_color"],
                                 dropdown_fg_color=self.theme["dropdown"]["dropdown_fg_color"],
                                 dropdown_hover_color=self.theme["dropdown"]["dropdown_hover_color"],
                                 button_color=self.theme["dropdown"]["button_color"],
                                 button_hover_color=self.theme["dropdown"]["button_hover_color"]) 

    def create_stats_section(self, parent):
        """Create the stats section for Today and This Week."""
        self.stats_container = ctk.CTkFrame(parent, fg_color=self.theme["stats_section"]["bg_color"], 
                                            corner_radius=12,
                                            border_width=1, 
                                            border_color=self.theme["stats_section"]["border_color"])
        self.stats_container.pack(fill="x", padx=20, pady=40)

        # Today’s Stats
        self.create_stat_row(self.stats_container, "Today", "00h 19m", "98%")

        # This Week’s Stats
        self.create_stat_row(self.stats_container, "This Week", "00h 19m", "98%", bottom_spacing=True)

    def create_stat_row(self, parent, label, time, percentage, bottom_spacing=False):
        """Create a single row in the stats section and store label references."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=(8, 15) if bottom_spacing else 8)

        # Store label references based on label name
        if label == "Today":
            self.today_label = ctk.CTkLabel(frame, text=label, font=("Roboto", 14), text_color=self.theme["text_color"])
            self.today_time_label = ctk.CTkLabel(frame, text=time, font=("Roboto", 14, "bold"), text_color=self.theme["text_color"])
        elif label == "This Week":
            self.week_label = ctk.CTkLabel(frame, text=label, font=("Roboto", 14), text_color=self.theme["text_color"])
            self.week_time_label = ctk.CTkLabel(frame, text=time, font=("Roboto", 14, "bold"), text_color=self.theme["text_color"])

        # Percentage label (unchanged)
        percentage_label = ctk.CTkLabel(frame, text=percentage, font=("Roboto", 14, "bold"), text_color=self.theme["play_button"]["fg_color"])
        
        # Pack labels
        if label == "Today":
            self.today_label.pack(side="left")
            self.today_time_label.pack(side="left", padx=10)
        elif label == "This Week":
            self.week_label.pack(side="left")
            self.week_time_label.pack(side="left", padx=10)

        percentage_label.pack(side="right")

    # Fetch projects asynchronously
        threading.Thread(target=self.fetch_projects, daemon=True).start()

    def fetch_projects(self):
        """Fetch project names from API and update dropdown safely."""
        try:
            response = requests.get("http://localhost:8080/api/project/projects")  
            if response.status_code == 200:
                projects = response.json()
                project_names = list(set(project["name"] for project in projects))  # ✅ Remove duplicates

                # ✅ Use `after()` to update the UI safely
                self.app.after(0, self.update_project_dropdown, project_names)
            else:
                self.app.after(0, self.update_project_dropdown, ["No Projects Assigned..."])
        except requests.exceptions.RequestException as e:
            print("Error fetching projects:", e)
            self.app.after(0, self.update_project_dropdown, ["No Projects Assigned..."])

    def update_project_dropdown(self, project_names):
        """Update the project dropdown in the main thread."""
        self.project_option_menu.configure(values=project_names)
        self.project_option_menu.set(project_names[0] if project_names else "No Projects Assigned...")


    def toggle_timer(self):
        """Toggle between start and stop."""
        if self.timer_running:
            self.stop_timer()
        else:
            self.start_timer()

    def start_timer(self):
        """Start the timer and capture random screenshots in a separate thread."""
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time() - self.elapsed_time
            self.uploader.capture_and_upload_screenshot(action="start")

            self.play_button.configure(text="■", fg_color=self.theme["stop_button"]["fg_color"], 
                                    hover_color=self.theme["stop_button"]["hover_color"])

            # ✅ Start random screenshot capture in a separate thread
            threading.Thread(target=self.capture_random_screenshots, daemon=True).start()

    def stop_timer(self):
        """Stop the timer and revert button appearance."""
        if self.timer_running:
            self.timer_running = False
            self.elapsed_time = time.time() - self.start_time
            self.uploader.capture_and_upload_screenshot(action="stop")

            self.play_button.configure(
                text="▶", 
                fg_color=self.theme["play_button"]["fg_color"], 
                hover_color=self.theme["play_button"]["hover_color"]
            )

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
        """Capture 5 random screenshots while the timer is running."""
        if not self.timer_running:
            return  # Exit if timer is stopped before it starts

        intervals = sorted(random.sample(range(1, 600), 5))  # ✅ Generate 5 random times within 10 minutes

        for interval in intervals:
            if not self.timer_running:
                break  # Stop immediately if timer is off

            #print(f"Waiting for {interval} seconds to capture a screenshot...")  # Debugging
            time.sleep(interval)  # ✅ Wait until this interval

            if not self.timer_running:
                break  # Stop immediately if timer is off

            print(f"Capturing random screenshot at {interval} seconds")  # Debugging
            self.uploader.capture_and_upload_screenshot(action="random")


    @staticmethod
    def format_time(seconds):
        """Convert seconds into HH:MM:SS format, ensuring leading zeroes."""
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}", f"{minutes:02}", f"{seconds:02}"  # Ensures leading zeroes