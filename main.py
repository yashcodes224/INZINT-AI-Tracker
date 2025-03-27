import customtkinter as ctk
from PIL import Image
import requests
from tkinter import messagebox
from components.task_tracker import TrackerApp
from utils.icon import resource_path
from dotenv import load_dotenv
import os
import sys
import json

# Determine the correct path for the .env file
if getattr(sys, 'frozen', False):  # If running as a bundled .exe
    env_path = os.path.join(sys._MEIPASS, '.env')  # Extracted folder path
else:
    env_path = '.env'  # If running from source, it's just the current directory

# Load the .env file
load_dotenv(env_path)

# Backend API URLs
API_LOGIN_URL = "https://o9bc4pbt8b.execute-api.ap-south-1.amazonaws.com/development/login"
API_SIGNUP_URL = "https://o9bc4pbt8b.execute-api.ap-south-1.amazonaws.com/development/signup"
API_PROFILE_URL = "https://o9bc4pbt8b.execute-api.ap-south-1.amazonaws.com/development/profile"  # Endpoint to fetch user details after login

# Define a secure hidden directory
SESSION_DIR = os.path.join(os.path.expanduser("~"), ".itrack")
SESSION_FILE = os.path.join(SESSION_DIR, "session.json")

class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("iTrack - Login")
        self.geometry("770x560")
        self.resizable(False, False)
        self.iconbitmap(resource_path("assets/logo2.ico"))  # Updated icon path

        # Set theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Store authentication details in memory
        self.auth_token = None
        self.user_role = None
        self.user_name = None

        # Set the window close protocol to use safe exit
        self.protocol("WM_DELETE_WINDOW", self._safe_exit)

        # Check if a session already exists
        if self.load_session():
            self.open_task_tracker()  # Skip login and go directly to tracker
        else:
            self.create_logo_section()
            self.create_login_form()

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

    def load_session(self):
        """Load session details from the hidden directory."""
        try:
            with open(SESSION_FILE, "r") as file:
                session_data = json.load(file)
                self.auth_token = session_data["token"]
                self.user_name = session_data["user_name"]
                self.user_role = session_data["user_role"]
                return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False  # No session found, proceed with login

    def create_logo_section(self):
        """Create the logo and welcome text."""
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(pady=10)

        # Load and display logo
        logo_image = ctk.CTkImage(Image.open(resource_path("assets/logo.png")), size=(100, 50))
        logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="")
        logo_label.pack()

        # Welcome Text
        welcome_label = ctk.CTkLabel(
            self,
            text="Please drop in your Login Credentials!",
            font=("Roboto", 18, "bold"),
        )
        welcome_label.pack(pady=10)

    def create_login_form(self):
        """Create the login form."""
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(pady=20)

        # Email Field
        email_label = ctk.CTkLabel(form_frame, text="Email", font=("Roboto", 14))
        email_label.grid(row=0, column=0, pady=10, sticky="w")
        self.email_entry = ctk.CTkEntry(form_frame, placeholder_text="user@example.com", width=300)
        self.email_entry.grid(row=0, column=1, pady=10, padx=10)

        # Password Field
        password_label = ctk.CTkLabel(form_frame, text="Password", font=("Roboto", 14))
        password_label.grid(row=1, column=0, pady=10, sticky="w")
        self.password_entry = ctk.CTkEntry(form_frame, placeholder_text="********", show="*", width=300)
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)

        # Login Button
        submit_button = ctk.CTkButton(
            self, text="Login", font=("Roboto", 14, "bold"), command=self.login, width=200, height=40,
            fg_color="#f43f5e", hover_color="#dc2626"
        )
        submit_button.pack(pady=10)

        # Signup Link
        signup_label = ctk.CTkLabel(
            self,
            text="No account yet? Sign Up Here!",
            font=("Roboto", 12, "underline", "bold"),
            text_color="#3b82f6",
            cursor="hand2",
        )
        signup_label.pack(pady=10)
        signup_label.bind("<Button-1>", lambda e: self.open_signup_page())

    def login(self):
        """Handle login process."""
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Email and password are required")
            return

        try:
            response = requests.post(API_LOGIN_URL, json={"email": email, "password": password})

            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("token")

                # Fetch user details from API instead of local storage
                self.fetch_user_profile()

            else:
                messagebox.showerror("Error", response.json().get("message", "Login failed"))

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")

    def fetch_user_profile(self):
        """Fetch user details from backend using the token and store session."""
        headers = {"Authorization": f"Bearer {self.auth_token}"}

        try:
            response = requests.get(API_PROFILE_URL, headers=headers)

            if response.status_code == 200:
                user_data = response.json()
                self.user_name = user_data.get("name")
                self.user_role = user_data.get("role", "User")

                # Save session locally
                self.save_session()

                messagebox.showinfo("Success", f"Welcome {self.user_name}! You are logged in as {self.user_role}.")
                self.open_task_tracker()

            else:
                messagebox.showerror("Error", "Failed to fetch user details from server.")

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")

    def save_session(self):
        """Save session details to a hidden directory."""
        if not os.path.exists(SESSION_DIR):
            os.makedirs(SESSION_DIR, exist_ok=True)  # Create directory if it doesn't exist

        session_data = {
            "token": self.auth_token,
            "user_name": self.user_name,
            "user_role": self.user_role
        }
    
        with open(SESSION_FILE, "w") as file:
            json.dump(session_data, file)

    def open_signup_page(self):
        """Open the signup page."""
        self.destroy()
        SignUpPage().mainloop()

    def open_task_tracker(self):
        """Open the task tracker page using in-memory token and role."""
        self.destroy()
        TrackerApp(token=self.auth_token, role=self.user_role, user_name=self.user_name).mainloop()
        # Set the proper close protocol for the tracker app
        TrackerApp.protocol("WM_DELETE_WINDOW", TrackerApp._safe_exit)
        
        self.destroy()  # Destroy login window
        TrackerApp.mainloop()  # Start tracker app's event loop

class SignUpPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("iTrack - Sign Up")
        self.geometry("770x560")
        self.resizable(False, False)
        self.iconbitmap(resource_path("assets/logo2.ico"))  # Updated icon path

        # Set theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # UI Components
        self.create_logo_section()
        self.create_signup_form()

    def create_logo_section(self):
        """Create the logo and welcome text."""
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(pady=10)

        # Load and display logo
        logo_image = ctk.CTkImage(Image.open(resource_path("assets/logo.png")), size=(100, 50))
        logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="")
        logo_label.pack()

        # Welcome Text
        welcome_label = ctk.CTkLabel(
            self,
            text="Create a new account",
            font=("Roboto", 18, "bold"),
        )
        welcome_label.pack(pady=10)

    def create_signup_form(self):
        """Create the signup form."""
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(pady=20)

        # Name Field
        name_label = ctk.CTkLabel(form_frame, text="Name", font=("Roboto", 14))
        name_label.grid(row=0, column=0, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(form_frame, placeholder_text="John Doe", width=300)
        self.name_entry.grid(row=0, column=1, pady=10, padx=10)

        # Email Field
        email_label = ctk.CTkLabel(form_frame, text="Email", font=("Roboto", 14))
        email_label.grid(row=1, column=0, pady=10, sticky="w")
        self.email_entry = ctk.CTkEntry(form_frame, placeholder_text="user@example.com", width=300)
        self.email_entry.grid(row=1, column=1, pady=10, padx=10)

        # Password Field
        password_label = ctk.CTkLabel(form_frame, text="Password", font=("Roboto", 14))
        password_label.grid(row=2, column=0, pady=10, sticky="w")
        self.password_entry = ctk.CTkEntry(form_frame, placeholder_text="********", show="*", width=300)
        self.password_entry.grid(row=2, column=1, pady=10, padx=10)

        # Role Selection Dropdown
        role_label = ctk.CTkLabel(form_frame, text="Role", font=("Roboto", 14))
        role_label.grid(row=3, column=0, pady=10, sticky="w")

        self.role_var = ctk.StringVar(value="User")  # Default role is "User"
        self.role_dropdown = ctk.CTkComboBox(form_frame, values=["User", "Admin"], variable=self.role_var, width=300)
        self.role_dropdown.grid(row=3, column=1, pady=10, padx=10)

        # Signup Button
        signup_button = ctk.CTkButton(
            self, text="Sign Up", font=("Roboto", 14, "bold"), command=self.signup, width=200, height=40,
            fg_color="#f43f5e", hover_color="#dc2626"
        )
        signup_button.pack(pady=10)

    def signup(self):
        """Handle signup process."""
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()

        try:
            response = requests.post(API_SIGNUP_URL, json={"name": name, "email": email, "password": password, "role": role})

            if response.status_code == 201:
                messagebox.showinfo("Success", "Signup successful! Please login.")
                self.destroy()
                LoginPage().mainloop()
            else:
                messagebox.showerror("Error", response.json().get("message", "Signup failed"))

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")


if __name__ == "__main__":
    LoginPage().mainloop()
