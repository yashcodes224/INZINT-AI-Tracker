import customtkinter as ctk
from PIL import Image
import json
import os
import task_tracker
from tkinter import messagebox  # Import tkinter messagebox


class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("iTrack")
        self.geometry("770x560")
        self.resizable(False, False)

        # Create the user.json file if it does not exist
        if not os.path.exists("user.json"):
            with open("user.json", "w") as f:
                json.dump({}, f)

        # Set custom fonts
        ctk.set_appearance_mode("light")  # Light mode
        ctk.set_default_color_theme("blue")

        # Add components
        self.create_logo_section()
        self.create_login_form()

    def create_logo_section(self):
        """Create the logo and welcome text."""
        # Logo Frame
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(pady=10)

        # Load and display the logo
        logo_image = ctk.CTkImage(Image.open("logo.png"), size=(100, 50))  # Adjust the logo path
        logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="")
        logo_label.pack()

        # Welcome Label
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

        # Email Entry
        email_label = ctk.CTkLabel(form_frame, text="Email", font=("Roboto", 14))
        email_label.grid(row=0, column=0, pady=10, sticky="w")
        self.email_entry = ctk.CTkEntry(form_frame, placeholder_text="user@example.com", width=300)
        self.email_entry.grid(row=0, column=1, pady=10, padx=10)

        # Password Entry
        password_label = ctk.CTkLabel(form_frame, text="Password", font=("Roboto", 14))
        password_label.grid(row=1, column=0, pady=10, sticky="w")
        self.password_entry = ctk.CTkEntry(form_frame, placeholder_text="********", show="*", width=300)
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)

        # Forgot Password Label
        forgot_password_label = ctk.CTkLabel(
            form_frame, text="Forgot password?", font=("Roboto", 12, "underline"), text_color="#3b82f6"
        )
        forgot_password_label.grid(row=2, column=1, sticky="e", pady=5)

        # Submit Button
        submit_button = ctk.CTkButton(
            self, text="Submit", font=("Roboto", 14, "bold"), command=self.login, width=200, height=40, fg_color="#f43f5e"
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
        signup_label.bind("<Button-1>", lambda e: self.signup())

    def login(self):
        """Handle the login process."""
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Load users from the JSON file
        with open("user.json", "r") as f:
            users = json.load(f)

        if email in users and users[email] == password:
            messagebox.showinfo("Success", "Login successful!")  # Use tkinter messagebox
            self.open_task_tracker()
        else:
            messagebox.showerror("Error", "Invalid email or password")  # Use tkinter messagebox

    def signup(self):
        """Handle the signup process."""
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Email and password are required")  # Use tkinter messagebox
            return

        # Load users from the JSON file
        with open("user.json", "r") as f:
            users = json.load(f)

        if email in users:
            messagebox.showerror("Error", "Email already exists")  # Use tkinter messagebox
        else:
            users[email] = password
            with open("user.json", "w") as f:
                json.dump(users, f)
            messagebox.showinfo("Success", "Signup successful!")  # Use tkinter messagebox
            self.open_task_tracker()

    def open_task_tracker(self):
        """Open the task tracker page."""
        self.destroy()
        task_tracker.TrackerApp().mainloop()


if __name__ == "__main__":
    app = LoginPage()
    app.iconbitmap('logo2.ico')
    app.mainloop()