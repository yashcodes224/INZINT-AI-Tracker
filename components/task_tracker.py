import customtkinter as ctk
from components.settings.settings import SettingsSection
from components.profile.profile import ProfileUI
from components.tasks.tasks import TasksSection
from components.timer.timer import TimerMixin
from components.sidebar.sidebar import Sidebar
from components.timer.timer_style import LIGHT_THEME, DARK_THEME 
import os 
from utils.icon import resource_path
from tkinter import TclError, messagebox

# Define the same secure hidden directory
SESSION_DIR = os.path.join(os.path.expanduser("~"), ".itrack")
SESSION_FILE = os.path.join(SESSION_DIR, "session.json")

class TrackerApp(ctk.CTk, TimerMixin):
    def __init__(self, token, role, user_name):
        super().__init__()

        self.token = token
        self.user_name = user_name  # ✅ Store user_name first
        self.role = role
        self.title("iTrack")
        self.iconbitmap(resource_path("assets/logo2.ico"))
        self.geometry("770x560")
        self.resizable(False, False)
        self.task_data = []

        # ✅ Default to Light Theme on Startup
        self.current_theme = "Light"
        self.theme = LIGHT_THEME  

        # Sidebar
        self.sidebar = Sidebar(self, self)

        # Left Section (Tasks, Profile, Settings)
        self.left_frame = ctk.CTkFrame(self, fg_color=self.theme["background"], corner_radius=0)
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.left_frame.pack_propagate(False)

        # Right Section (Timer)
        self.right_frame = ctk.CTkFrame(self, fg_color=self.theme["background"], corner_radius=0)
        self.right_frame.pack(side="right", fill="both", expand=True)
        self.right_frame.pack_propagate(False)

        # ✅ Initialize TimerMixin AFTER right_frame is created
        TimerMixin.__init__(self, self, user_name=self.user_name)

        # Load Initial Page (Tasks)
        self.show_tasks()

        # ✅ Now it's safe to create the Timer UI
        self.create_timer_section(self.right_frame)

    def set_theme(self, theme):
        """Set and apply theme instantly across the app from settings.py."""
        if theme in ["Light", "Dark"]:
            self.current_theme = theme
            self.theme = LIGHT_THEME if theme == "Light" else DARK_THEME
            self.apply_theme()

    def apply_theme(self):
        """Apply the selected theme globally without affecting timer functionality."""
        self.configure(fg_color=self.theme["background"])

        if hasattr(self, "left_frame") and hasattr(self, "right_frame"):
            self.left_frame.configure(fg_color=self.theme["background"])
            self.right_frame.configure(fg_color=self.theme["background"])

        # ✅ Update Sidebar (if applicable)
        if hasattr(self.sidebar, "apply_theme"):
            self.sidebar.apply_theme()

        # ✅ Update the currently displayed section (Tasks, Profile, or Settings)
        if self.left_frame.winfo_children():
            current_page = self.left_frame.winfo_children()[0]
            if isinstance(current_page, TasksSection):
                self.show_tasks()
            elif isinstance(current_page, ProfileUI):
                self.show_profile()
            elif isinstance(current_page, SettingsSection):
                self.show_settings()
        # ✅ Apply theme to the timer UI using TimerMixin
        self.update_timer_theme()

    def clear_left_frame(self):
        """Clear only the left section while keeping the Timer UI on the right unchanged."""
        for widget in self.left_frame.winfo_children():
            widget.destroy()

    def show_profile(self):
        """Switch to Profile UI while keeping the Timer UI fixed."""
        self.clear_left_frame()
        ProfileUI(self.left_frame, self, self.token).pack(fill="both", expand=True)

    def show_tasks(self):
        """Switch to Tasks UI while keeping the Timer UI fixed."""
        self.clear_left_frame()
        TasksSection(self.left_frame, self, self.token).pack(fill="both", expand=True)

    def show_settings(self):
        """Switch to Settings UI while keeping the Timer UI fixed."""
        self.clear_left_frame()
        settings_page = SettingsSection(self.left_frame, self)
        settings_page.pack(fill="both", expand=True)

    def sign_out(self):
        """Handle user logout and clear saved session."""
        # Stop any active timers first
        if hasattr(self, 'stop_timer') and callable(self.stop_timer):
            self.stop_timer()  # Stop timer if running
        
        # Remove session file to ensure login appears on next start
        if os.path.exists(SESSION_FILE):
            try:
                os.remove(SESSION_FILE)  # Delete saved session
            except Exception as e:
                print(f"Error removing session file: {e}")
        
        # Show message
        messagebox.showinfo("Logged Out", "You have been logged out successfully.")
        
        # Schedule the application exit after the messagebox is closed
        # This helps avoid race conditions by giving time for message box to close
        self.after(200, self._safe_exit)

    def _safe_exit(self):
        """Safely exit the application to avoid tkinter errors."""
        try:
            # Disable all event handlers
            self.unbind_all("<Button>")
            self.unbind_all("<Key>")
            
            # Destroy all top-level windows
            for widget in self.winfo_children():
                try:
                    widget.destroy()
                except Exception:
                    pass
                    
            # Exit the application
            self.quit()
            self.destroy()
            
            # Force exit as last resort
            import os, sys
            os._exit(0)  # Force exit without cleanup
        except Exception as e:
            print(f"Error during exit: {e}")
            os._exit(0)  # Force exit as fallback

if __name__ == "__main__":
    try:
        app = TrackerApp(token="your_token_here", role="your_role_here", user_name="your_name_here")
        app.protocol("WM_DELETE_WINDOW", lambda: app._safe_exit())  # Properly handle window closing
        app.mainloop()
    except TclError as e:
        # Log the error for debugging
        print(f"TclError: {e}")
        pass