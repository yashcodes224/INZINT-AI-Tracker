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

# class PasswordEntry(ctk.CTkFrame):
#     def __init__(self, master, placeholder_text="********", width=350, **kwargs):
#         super().__init__(master, fg_color="transparent", **kwargs)

#         self.password_hidden = True
        
#         # Container frame for password field and button
#         self.container = ctk.CTkFrame(self, fg_color="#F8FAFC", corner_radius=6)
#         self.container.pack(fill="x", expand=True)
        
#         # Password entry
#         self.password_entry = ctk.CTkEntry(
#             self.container,
#             placeholder_text=placeholder_text,
#             show="●",
#             width=width - 40,  # Account for button width
#             height=45,  # Match email entry height
#             border_width=0,
#             fg_color="transparent"
#         )
#         self.password_entry.pack(side="left", padx=(5, 0), pady=2)
        
#         # Toggle button with both icons
#         self.eye_open = "👁"
#         self.eye_closed = "👁‍🗨"
#         self.toggle_btn = ctk.CTkButton(
#             self.container,
#             text=self.eye_closed,
#             width=30,
#             height=30,
#             command=self.toggle_password_visibility,
#             fg_color="transparent",
#             hover_color="#E2E8F0",
#             text_color="#64748B"
#         )
#         self.toggle_btn.pack(side="right", padx=5, pady=2)

#     def toggle_password_visibility(self):
#         self.password_hidden = not self.password_hidden
#         self.password_entry.configure(show="●" if self.password_hidden else "")
#         self.toggle_btn.configure(text=self.eye_closed if self.password_hidden else self.eye_open)
        
#     def get(self):
#         return self.password_entry.get()

# class LoginPage(ctk.CTk):
#     def __init__(self):
#         super().__init__()

#         # Window configuration
#         self.title("iTrack - Login")
#         self.geometry("1000x600")
#         self.resizable(False, False)
#         self.iconbitmap('assets/logo2.ico')

#         # Create user.json if it does not exist
#         if not os.path.exists("user.json"):
#             with open("user.json", "w") as f:
#                 json.dump({}, f)

#         # Set theme
#         ctk.set_appearance_mode("light")
#         ctk.set_default_color_theme("blue")

#         # Create split layout
#         self.create_split_layout()

#     def create_split_layout(self):
#         # Left sidebar (1/4 width) - Red background
#         sidebar = ctk.CTkFrame(self, fg_color="#f43f5e", width=250, corner_radius=0)
#         sidebar.pack(side="left", fill="y")
#         sidebar.pack_propagate(False)

#         # Logo in sidebar
#         logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
#         logo_frame.pack(pady=(60, 0))
        
#         logo_image = ctk.CTkImage(Image.open("assets/logo.png"), size=(150, 75))
#         logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="")
#         logo_label.pack()

#         # Main content area (3/4 width) - Light background
#         main_area = ctk.CTkFrame(self, fg_color="#F1F5F9")
#         main_area.pack(side="left", fill="both", expand=True)

#         # Content container
#         self.content_frame = ctk.CTkFrame(main_area, fg_color="#FFFFFF", corner_radius=15)
#         self.content_frame.pack(padx=50, pady=30, fill="both", expand=True)

#         self.create_login_form()

#     def create_login_form(self):
#         """Create the login form."""
#         # Welcome Text
#         welcome_label = ctk.CTkLabel(
#             self.content_frame,
#             text="Welcome back!",
#             font=("Inter", 28, "bold"),
#             text_color="#1F2937"
#         )
#         welcome_label.pack(pady=(40, 5))

#         subtitle_label = ctk.CTkLabel(
#             self.content_frame,
#             text="Please enter your credentials to access your account",
#             font=("Inter", 14),
#             text_color="#64748B"
#         )
#         subtitle_label.pack(pady=(0, 40))

#         # Form container
#         form_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
#         form_frame.pack(pady=20)

#         # Email Field
#         email_label = ctk.CTkLabel(
#             form_frame,
#             text="Email Address",
#             font=("Inter", 14, "bold"),
#             text_color="#374151"
#         )
#         email_label.grid(row=0, column=0, pady=(0, 5), sticky="w")
        
#         self.email_entry = ctk.CTkEntry(
#             form_frame,
#             placeholder_text="user@example.com",
#             width=350,
#             height=45,
#             fg_color="#F8FAFC",
#             border_width=0
#         )
#         self.email_entry.grid(row=1, column=0, pady=(0, 20))

#         # Password Field
#         password_label = ctk.CTkLabel(
#             form_frame,
#             text="Password",
#             font=("Inter", 14, "bold"),
#             text_color="#374151"
#         )
#         password_label.grid(row=2, column=0, pady=(0, 5), sticky="w")
        
#         self.password_entry = PasswordEntry(form_frame, width=350)
#         self.password_entry.grid(row=3, column=0, pady=(0, 20))

#         # Buttons container
#         button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
#         button_frame.grid(row=4, column=0, pady=(20, 0))

#         # Login Button
#         submit_button = ctk.CTkButton(
#             button_frame,
#             text="Sign In",
#             font=("Inter", 14, "bold"),
#             command=self.login,
#             width=350,
#             height=45,
#             fg_color="#f43f5e",
#             hover_color="#dc2626",
#             corner_radius=6
#         )
#         submit_button.pack(pady=(0, 10))

#         # Sign Up Button
#         signup_button = ctk.CTkButton(
#             button_frame,
#             text="Create Account",
#             font=("Inter", 14, "bold"),
#             command=self.open_signup_page,
#             width=350,
#             height=45,
#             fg_color="#F8FAFC",
#             hover_color="#E2E8F0",
#             text_color="#64748B",
#             corner_radius=6
#         )
#         signup_button.pack()

#     def login(self):
#         """Handle login process."""
#         email = self.email_entry.get()
#         password = self.password_entry.get()

#         if not email or not password:
#             messagebox.showerror("Error", "Please fill in all fields")
#             return

#         try:
#             response = requests.post(API_LOGIN_URL, json={"email": email, "password": password})

#             if response.status_code == 200:
#                 data = response.json()
#                 token = data.get("token")
#                 with open("user.json", "w") as f:
#                     json.dump({"email": email, "token": token}, f)
#                 self.open_task_tracker(token)
#             else:
#                 messagebox.showerror("Error", "Invalid email or password")

#         except requests.RequestException as e:
#             messagebox.showerror("Error", "Failed to connect to server. Please try again.")

#     def open_signup_page(self):
#         """Open the signup page."""
#         self.destroy()
#         SignUpPage().mainloop()

#     def open_task_tracker(self, token):
#         """Open the task tracker page."""
#         self.destroy()
#         TrackerApp(token=token).mainloop()

# class SignUpPage(ctk.CTk):
#     def __init__(self):
#         super().__init__()

#         # Window configuration
#         self.title("iTrack - Sign Up")
#         self.geometry("1000x600")
#         self.resizable(False, False)
#         self.iconbitmap('assets/logo2.ico')

#         # Set theme
#         ctk.set_appearance_mode("light")
#         ctk.set_default_color_theme("blue")

#         # Create split layout
#         self.create_split_layout()

#     def create_split_layout(self):
#         # Left sidebar (1/4 width) - Red background
#         sidebar = ctk.CTkFrame(self, fg_color="#f43f5e", width=250, corner_radius=0)
#         sidebar.pack(side="left", fill="y")
#         sidebar.pack_propagate(False)

#         # Logo in sidebar
#         logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
#         logo_frame.pack(pady=(60, 0))
        
#         logo_image = ctk.CTkImage(Image.open("assets/logo.png"), size=(150, 75))
#         logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="")
#         logo_label.pack()

#         # Main content area (3/4 width) - Light background
#         main_area = ctk.CTkFrame(self, fg_color="#F1F5F9")
#         main_area.pack(side="left", fill="both", expand=True)

#         # Content container
#         self.content_frame = ctk.CTkFrame(main_area, fg_color="#FFFFFF", corner_radius=15)
#         self.content_frame.pack(padx=50, pady=20, fill="both", expand=True)

#         self.create_signup_form()

#     def create_signup_form(self):
#         """Create the signup form."""
#         # Welcome Text
#         welcome_label = ctk.CTkLabel(
#             self.content_frame,
#             text="Create your account",
#             font=("Inter", 28, "bold"),
#             text_color="#1F2937"
#         )
#         welcome_label.pack(pady=(40, 5))

#         subtitle_label = ctk.CTkLabel(
#             self.content_frame,
#             text="Enter your information to get started",
#             font=("Inter", 14),
#             text_color="#64748B"
#         )
#         subtitle_label.pack(pady=(0, 40))

#         # Form container
#         form_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
#         form_frame.pack(pady=20)

#         # Name Field
#         name_label = ctk.CTkLabel(
#             form_frame,
#             text="Full Name",
#             font=("Inter", 14, "bold"),
#             text_color="#374151"
#         )
#         name_label.grid(row=0, column=0, pady=(0, 5), sticky="w")
        
#         self.name_entry = ctk.CTkEntry(
#             form_frame,
#             placeholder_text="John Doe",
#             width=350,
#             height=45,
#             fg_color="#F8FAFC",
#             border_width=0
#         )
#         self.name_entry.grid(row=1, column=0, pady=(0, 20))

#         # Email Field
#         email_label = ctk.CTkLabel(
#             form_frame,
#             text="Email Address",
#             font=("Inter", 14, "bold"),
#             text_color="#374151"
#         )
#         email_label.grid(row=2, column=0, pady=(0, 5), sticky="w")
        
#         self.email_entry = ctk.CTkEntry(
#             form_frame,
#             placeholder_text="user@example.com",
#             width=350,
#             height=45,
#             fg_color="#F8FAFC",
#             border_width=0
#         )
#         self.email_entry.grid(row=3, column=0, pady=(0, 20))

#         # Password Field
#         password_label = ctk.CTkLabel(
#             form_frame,
#             text="Password",
#             font=("Inter", 14, "bold"),
#             text_color="#374151"
#         )
#         password_label.grid(row=4, column=0, pady=(0, 5), sticky="w")
        
#         self.password_entry = PasswordEntry(form_frame, width=350)
#         self.password_entry.grid(row=5, column=0, pady=(0, 20))

#         # Buttons container
#         button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
#         button_frame.grid(row=6, column=0, pady=(20, 0))

#         # Sign Up Button
#         signup_button = ctk.CTkButton(
#             button_frame,
#             text="Create Account",
#             font=("Inter", 14, "bold"),
#             command=self.signup,
#             width=350,
#             height=45,
#             fg_color="#f43f5e",
#             hover_color="#dc2626",
#             corner_radius=6
#         )
#         signup_button.pack(pady=(0, 10))

#         # Login Button
#         login_button = ctk.CTkButton(
#             button_frame,
#             text="Back to Login",
#             font=("Inter", 14, "bold"),
#             command=self.open_login_page,
#             width=350,
#             height=45,
#             fg_color="#F8FAFC",
#             hover_color="#E2E8F0",
#             text_color="#64748B",
#             corner_radius=6
#         )
#         login_button.pack()

#     def signup(self):
#         """Handle signup process."""
#         name = self.name_entry.get()
#         email = self.email_entry.get()
#         password = self.password_entry.get()

#         if not name or not email or not password:
#             messagebox.showerror("Error", "Please fill in all fields")
#             return

#         try:
#             response = requests.post(API_SIGNUP_URL, json={
#                 "name": name,
#                 "email": email,
#                 "password": password
#             })
            
#             if response.status_code == 201:
#                 messagebox.showinfo("Success", "Account created successfully!")
#                 self.open_login_page()
#             else:
#                 messagebox.showerror("Error", response.json().get("message", "Registration failed"))

#         except requests.RequestException as e:
#             messagebox.showerror("Error", "Failed to connect to server. Please try again.")

#     def open_login_page(self):
#         """Open the login page."""
#         self.destroy()
#         LoginPage().mainloop()

# if __name__ == "__main__":
#     LoginPage().mainloop()