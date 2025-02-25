import customtkinter as ctk
from PIL import Image
import requests
from tkinter import messagebox
from components.task_tracker import TrackerApp

# Backend API URLs
API_LOGIN_URL = "http://localhost:8080/auth/login"
API_SIGNUP_URL = "http://localhost:8080/auth/signup"
API_PROFILE_URL = "http://localhost:8080/auth/profile"  # Endpoint to fetch user details after login


class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("iTrack - Login")
        self.geometry("770x560")
        self.resizable(False, False)
        self.iconbitmap('assets/logo2.ico')

        # Set theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # UI Components
        self.create_logo_section()
        self.create_login_form()

        # Store authentication details in memory
        self.auth_token = None
        self.user_role = None
        self.user_name = None

    def create_logo_section(self):
        """Create the logo and welcome text."""
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(pady=10)

        # Load and display logo
        logo_image = ctk.CTkImage(Image.open("assets/logo.png"), size=(100, 50))
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
        """Fetch user details from backend using the token."""
        headers = {"Authorization": f"Bearer {self.auth_token}"}

        try:
            response = requests.get(API_PROFILE_URL, headers=headers)

            if response.status_code == 200:
                user_data = response.json()
                self.user_name = user_data.get("name")
                self.user_role = user_data.get("role", "User")  # Default to 'User' if not provided

                messagebox.showinfo("Success", f"Welcome {self.user_name}! You are logged in as {self.user_role}.")
                self.open_task_tracker()

            else:
                messagebox.showerror("Error", "Failed to fetch user details from server.")

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")

    def open_signup_page(self):
        """Open the signup page."""
        self.destroy()
        SignUpPage().mainloop()

    def open_task_tracker(self):
        """Open the task tracker page using in-memory token and role."""
        self.destroy()
        TrackerApp(token=self.auth_token, role=self.user_role, user_name=self.user_name).mainloop()


class SignUpPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("iTrack - Sign Up")
        self.geometry("770x560")
        self.resizable(False, False)
        self.iconbitmap('assets/logo2.ico')

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
        logo_image = ctk.CTkImage(Image.open("assets/logo.png"), size=(100, 50))
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
        """Create the signup form (same as before)."""
        # (Keep this unchanged)

    def signup(self):
        """Handle signup process."""
        # (Keep this unchanged)


if __name__ == "__main__":
    LoginPage().mainloop()
