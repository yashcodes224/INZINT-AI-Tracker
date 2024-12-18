import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os
import task_tracker  # Import the task tracker module


class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("INZINT")
        self.geometry("770x560")
        self.resizable(False, False)
        self.configure(bg="white")

        # Create the user.json file if it does not exist
        if not os.path.exists("user.json"):
            with open("user.json", "w") as f:
                json.dump({}, f)

        # Logo Section
        self.create_logo_section()

        # Login Form Section
        self.create_login_form()

    def create_logo_section(self):
        """Create the logo at the top."""
        logo_frame = tk.Frame(self, bg="white")
        logo_frame.pack(pady=20)

        # Load the INZINT logo
        logo_image = Image.open("logo.png")  # Replace with the file path of your logo
        logo_image = logo_image.resize((100, 50), Image.Resampling.LANCZOS)  # Resize to fit
        logo_photo = ImageTk.PhotoImage(logo_image)

        logo_label = tk.Label(logo_frame, image=logo_photo, bg="white")
        logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
        logo_label.pack()

        # Welcome Text (placed just below the logo)
        welcome_label = tk.Label(
            self, text="Welcome to INZINT Family..!!", font=("EB Garamond", 24, "bold"), bg="white", fg="#333"
        )
        welcome_label.pack(pady=10)

    def create_login_form(self):
        """Create the login form section."""
        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(pady=20)

        # Email Entry
        email_label = tk.Label(form_frame, text="Email", font=("Montserrat", 12), bg="white", fg="#333")
        email_label.grid(row=1, column=0, pady=10, sticky="e", padx=10)
        self.email_entry = self.create_styled_entry(form_frame, "Enter your email", 1)

        # Password Entry
        password_label = tk.Label(form_frame, text="Password", font=("Montserrat", 12), bg="white", fg="#333")
        password_label.grid(row=2, column=0, pady=10, sticky="e", padx=10)
        self.password_entry = self.create_styled_entry(form_frame, "Enter your password", 2, show="*")

        forgot_password_label = tk.Label(
            form_frame,
            text="Forgot Password?",
            font=("Arial", 10, "underline"),
            fg="#00b8d4",
            cursor="hand2",
            bg="white",
        )
        forgot_password_label.grid(row=3, column=1, sticky="e", pady=(0, 10))

        # Buttons with rounded corners
        signin_button = tk.Button(
            self,
            text="Sign In",
            bg="#3b82f6",
            fg="white",
            font=("Arial", 12),
            width=30,
            height=2,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#3b82f6",
            borderwidth=2,
            command=self.login
        )
        signin_button.pack(pady=(0,10))

        # "Don't have an account?" label
        no_account_label = tk.Label(
            self,
            text="Don't have an account?",
            font=("Arial", 10, "underline"),
            fg="#333",
            cursor="mouse",
            bg="white",
        )
        no_account_label.pack(pady=(30,0))  # Add space between Sign In button and this label

        signup_button = tk.Button(
            self,
            text="Sign Up",
            bg="#10b981",
            fg="white",
            font=("Arial", 12),
            width=20,
            height=2,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#10b981",
            borderwidth=2,
            command=self.signup
        )
        signup_button.pack(pady=(5,30))

    def create_styled_entry(self, parent, placeholder, row, show=None):
        """Creates a styled entry box with placeholder text effect, rounded corners, and visible borders."""
        # Frame to hold the Entry widget, simulating a border
        entry_frame = tk.Frame(parent, bg="white", highlightbackground="#ccc", highlightthickness=1, bd=0)
        entry_frame.grid(row=row, column=1, pady=10, padx=10, sticky="w")

        # Entry widget inside the frame
        entry = tk.Entry(entry_frame, font=("Arial", 12), width=30, show=show, relief="flat", bg="white", bd=0)
        entry.pack(padx=5, pady=5)

        # Entry Style (grayish color with rounded corners)
        entry.insert(0, placeholder)  # Set placeholder text
        entry.config(fg="gray")  # Set placeholder color

        # Bind events to make the placeholder text disappear/appear on focus
        entry.bind("<FocusIn>", lambda e, entry=entry, placeholder=placeholder: self.on_focus_in(entry, placeholder))
        entry.bind("<FocusOut>", lambda e, entry=entry, placeholder=placeholder: self.on_focus_out(entry, placeholder))

        return entry

    def on_focus_in(self, entry, placeholder):
        """Clear placeholder text when entry is focused."""
        if entry.get() == placeholder:  # If it's the placeholder text
            entry.delete(0, tk.END)  # Clear the text
            entry.config(fg="black")  # Change text color to black

    def on_focus_out(self, entry, placeholder):
        """Restore placeholder text if the entry is empty."""
        if entry.get() == "":  # If user leaves the box empty
            entry.insert(0, placeholder)  # Reinsert the placeholder text
            entry.config(fg="gray")  # Make it look like placeholder again

    def login(self):
        """Logic for user login"""
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Load users from the JSON file
        with open("user.json", "r") as f:
            users = json.load(f)

        if email in users and users[email] == password:
            self.show_message("Login successful!", "success")
            self.open_task_tracker()
        else:
            self.show_message("Invalid email or password", "error")

    def signup(self):
        """Logic for user signup"""
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            self.show_message("Email and password are required", "error")
            return

        # Load users from the JSON file
        with open("user.json", "r") as f:
            users = json.load(f)

        if email in users:
            self.show_message("Email already exists", "error")
        else:
            users[email] = password
            with open("user.json", "w") as f:
                json.dump(users, f)
            self.show_message("Signup successful!", "success")
            self.open_task_tracker()

    def open_task_tracker(self):
        """Open the Task Tracker page"""
        self.destroy()  # Close the current window (LoginPage)
        task_tracker.TrackerApp().mainloop()  # Open Task Tracker app

    def show_message(self, message, message_type):
        """Display a message box (popup dialog)"""
        if message_type == "success":
            messagebox.showinfo("Success", message)
        elif message_type == "error":
            messagebox.showerror("Error", message)


if __name__ == "__main__":
    app = LoginPage()
    app.iconbitmap('logo2.ico')  # Make sure to set a valid icon path
    app.mainloop()
