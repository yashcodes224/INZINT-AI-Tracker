import customtkinter as ctk
from PIL import Image
import json
import os
import requests
from tkinter import messagebox
from components.task_tracker import TrackerApp

# Backend API URLs
API_LOGIN_URL = "http://localhost:8080/api/auth/login"
API_SIGNUP_URL = "http://localhost:8080/api/auth/signup"


class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("iTrack - Login")
        self.geometry("770x560")
        self.resizable(False, False)
        self.iconbitmap('assets/logo2.ico')

        # Create user.json if it does not exist
        if not os.path.exists("user.json"):
            with open("user.json", "w") as f:
                json.dump({}, f)

        # Set theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # UI Components
        self.create_logo_section()
        self.create_login_form()

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
                token = data.get("token")
                with open("user.json", "w") as f:
                    json.dump({"email": email, "token": token}, f)
                messagebox.showinfo("Success", "Login successful!")
                self.open_task_tracker(token)
            else:
                messagebox.showerror("Error", response.json().get("message", "Login failed"))

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")

    def open_signup_page(self):
        """Open the signup page."""
        self.destroy()
        SignUpPage().mainloop()

    def open_task_tracker(self, token):
        """Open the task tracker page."""
        self.destroy()
        TrackerApp(token=token).mainloop()


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

        try:
            response = requests.post(API_SIGNUP_URL, json={"name": name, "email": email, "password": password})
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


# import customtkinter as ctk
# from PIL import Image
# import json
# import os
# import requests
# from tkinter import messagebox
# from components.task_tracker import TrackerApp

# # Backend API URLs
# API_LOGIN_URL = "http://localhost:8080/api/auth/login"
# API_SIGNUP_URL = "http://localhost:8080/api/auth/signup"


# class LoginPage(ctk.CTk):
#     def __init__(self):
#         super().__init__()

#         # Window configuration
#         self.title("iTrack - Login")
#         self.geometry("770x560")
#         self.resizable(False, False)
#         self.iconbitmap('assets/logo2.ico')

#         # Set theme
#         ctk.set_appearance_mode("light")
#         ctk.set_default_color_theme("blue")

#         # UI Components
#         self.create_logo_section()
#         self.create_login_form()

#     def login(self):
#         """Handle login process."""
#         email = self.email_entry.get()
#         password = self.password_entry.get()

#         if not email or not password:
#             messagebox.showerror("Error", "Email and password are required")
#             return

#         try:
#             response = requests.post(API_LOGIN_URL, json={"email": email, "password": password})

#             if response.status_code == 200:
#                 data = response.json()
#                 token = data.get("token")
#                 with open("user.json", "w") as f:
#                     json.dump({"email": email, "token": token}, f)
#                 messagebox.showinfo("Success", "Login successful!")
#                 self.open_task_tracker(token)
#             else:
#                 messagebox.showerror("Error", response.json().get("message", "Login failed"))

#         except requests.RequestException as e:
#             messagebox.showerror("Error", f"Failed to connect to server: {e}")

#     def create_logo_section(self):
#         """Create the logo and welcome text."""
#         logo_frame = ctk.CTkFrame(self, fg_color="transparent")
#         logo_frame.pack(pady=10)

#         # Load and display logo
#         logo_image = ctk.CTkImage(Image.open("assets/logo.png"), size=(100, 50))  
#         logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="") 
#         logo_label.pack()

#         # Welcome Text
#         welcome_label = ctk.CTkLabel(
#             self,
#             text="Welcome Back! Log in to continue.",
#             font=("Roboto", 20, "bold"),
#             text_color="#1E293B"
#         )
#         welcome_label.pack(pady=5)

#     def create_login_form(self):
#         """Create a professional login form inside a card-style frame."""
#         form_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
#         form_frame.pack(pady=20, padx=50)

#         # Email Field
#         self.create_input_field(form_frame, "Email", "user@example.com")

#         # Password Field with Eye Button
#         self.create_password_field(form_frame, "Password")

#         # Login Button (Hover Effect)
#         submit_button = ctk.CTkButton(
#             form_frame, text="Login", font=("Roboto", 14, "bold"), command=self.login, width=320, height=40,
#             fg_color="#f43f5e", hover_color="#e11d48", corner_radius=8
#         )
#         submit_button.pack(pady=15)

#         # Signup Link (Hover Effect)
#         signup_label = ctk.CTkLabel(
#             form_frame,
#             text="No account yet? Sign Up Here!",
#             font=("Roboto", 12, "underline", "bold"),
#             text_color="#3b82f6",
#             cursor="hand2",
#         )
#         signup_label.pack(pady=10)
#         signup_label.bind("<Button-1>", lambda e: self.open_signup_page())
#         signup_label.bind("<Enter>", lambda e: signup_label.configure(text_color="#2563eb"))
#         signup_label.bind("<Leave>", lambda e: signup_label.configure(text_color="#3b82f6"))

#     def create_input_field(self, parent, label_text, placeholder):
#         """Reusable function for text input fields."""
#         label = ctk.CTkLabel(parent, text=label_text, font=("Roboto", 14))
#         label.pack(anchor="w", padx=20, pady=(10, 5))

#         entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=320, border_width=1, corner_radius=8)
#         entry.pack(anchor="w", padx=20, pady=5)
#         entry.bind("<FocusIn>", lambda e: entry.configure(border_color="#3b82f6"))
#         entry.bind("<FocusOut>", lambda e: entry.configure(border_color="#E5E7EB"))

#     def create_password_field(self, parent, label_text):
#         """Create a password entry with an eye button inside the box."""
#         label = ctk.CTkLabel(parent, text=label_text, font=("Roboto", 14))
#         label.pack(anchor="w", padx=20, pady=(10, 5))

#         # Password Entry
#         self.password_entry = ctk.CTkEntry(parent, placeholder_text="********", show="*", width=320, border_width=1, corner_radius=8)
#         self.password_entry.pack(anchor="w", padx=20, pady=5)

#         # Eye Button (Inside Entry)
#         self.show_password = False
#         self.eye_button = ctk.CTkLabel(parent, text="👁", font=("Arial", 14), cursor="hand2", text_color="#64748B",  fg_color="transparent")
#         self.eye_button.place(in_=self.password_entry, relx=0.92, rely=0.5, anchor="center")  # Inside the password box
#         self.eye_button.bind("<Button-1>", lambda e: self.toggle_password_visibility())

#     def toggle_password_visibility(self):
#         """Toggle password visibility."""
#         self.show_password = not self.show_password
#         self.password_entry.configure(show="" if self.show_password else "*")
#         self.eye_button.configure(text="🙈" if self.show_password else "👁")  # Toggle icon

#     def open_signup_page(self):
#         """Open the signup page."""
#         self.destroy()
#         SignUpPage().mainloop()

# class SignUpPage(ctk.CTk):
#     def __init__(self):
#         super().__init__()

#         # Window configuration
#         self.title("iTrack - Sign Up")
#         self.geometry("770x560")
#         self.resizable(False, False)
#         self.iconbitmap('assets/logo2.ico')

#         # Set theme
#         ctk.set_appearance_mode("light")
#         ctk.set_default_color_theme("blue")

#         # UI Components
#         self.create_logo_section()
#         self.create_signup_form()

#     def create_logo_section(self):
#         """Create the logo and welcome text."""
#         logo_frame = ctk.CTkFrame(self, fg_color="transparent")
#         logo_frame.pack(pady=10)

#         # Load and display logo
#         logo_image = ctk.CTkImage(Image.open("assets/logo.png"), size=(100, 50))  
#         logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="") 
#         logo_label.pack()

#         # Welcome Text
#         welcome_label = ctk.CTkLabel(
#             self,
#             text="Create a new account",
#             font=("Roboto", 20, "bold"),
#             text_color="#1E293B"
#         )
#         welcome_label.pack(pady=5)

#     def create_signup_form(self):
#         """Create a professional signup form inside a card-style frame."""
#         form_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=12, border_width=1, border_color="#E5E7EB")
#         form_frame.pack(pady=20, padx=50)

#         # Name Field
#         self.create_input_field(form_frame, "Name", "John Doe")

#         # Email Field
#         self.create_input_field(form_frame, "Email", "user@example.com")

#         # Password Field with Eye Button
#         self.create_password_field(form_frame, "Password")

#         # Signup Button
#         signup_button = ctk.CTkButton(
#             form_frame, text="Sign Up", font=("Roboto", 14, "bold"), command=self.signup, width=320, height=40,
#             fg_color="#f43f5e", hover_color="#e11d48", corner_radius=8
#         )
#         signup_button.pack(pady=15)

#     def create_input_field(self, parent, label_text, placeholder):
#         """Reusable function for text input fields."""
#         label = ctk.CTkLabel(parent, text=label_text, font=("Roboto", 14))
#         label.pack(anchor="w", padx=20, pady=(10, 5))

#         entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=320, border_width=1, corner_radius=8)
#         entry.pack(anchor="w", padx=20, pady=5)
#         entry.bind("<FocusIn>", lambda e: entry.configure(border_color="#3b82f6"))
#         entry.bind("<FocusOut>", lambda e: entry.configure(border_color="#E5E7EB"))

#     def create_password_field(self, parent, label_text):
#         """Create a password entry with an eye button inside the box."""
#         label = ctk.CTkLabel(parent, text=label_text, font=("Roboto", 14))
#         label.pack(anchor="w", padx=20, pady=(10, 5))

#         # Password Entry
#         self.password_entry = ctk.CTkEntry(parent, placeholder_text="********", show="*", width=320, border_width=1, corner_radius=8)
#         self.password_entry.pack(anchor="w", padx=20, pady=5)

#         # Eye Button (Inside Entry)
#         self.show_password = False
#         self.eye_button = ctk.CTkLabel(parent, text="👁", font=("Arial", 14), cursor="hand2", text_color="#64748B",  fg_color="transparent")
#         self.eye_button.place(in_=self.password_entry, relx=0.92, rely=0.5, anchor="center")  # Inside the password box
#         self.eye_button.bind("<Button-1>", lambda e: self.toggle_password_visibility())

#     def toggle_password_visibility(self):
#         """Toggle password visibility."""
#         self.show_password = not self.show_password
#         self.password_entry.configure(show="" if self.show_password else "*")
#         self.eye_button.configure(text="🙈" if self.show_password else "👁")  # Toggle icon

#     def signup(self):
#         """Handle signup process."""
#         messagebox.showinfo("Success", "Signup successful! Please login.")
#         self.destroy()
#         LoginPage().mainloop()


# if __name__ == "__main__":
#     LoginPage().mainloop()

