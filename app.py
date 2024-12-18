import tkinter as tk
from tkinter import messagebox
import json

# File to store user data
USER_DATA_FILE = "users.json"

# Utility to load user data
def load_users():
    try:
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Utility to save user data
def save_users(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file)

class TrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tracker App")
        self.geometry("770x560")
        self.resizable(False, False)

        # User Data
        self.users = load_users()

        # Theme State (default is light mode)
        self.theme = "light"
        self.themes = {
            "light": {"bg": "white", "fg": "black", "button_bg": "#e0e0e0", "button_fg": "black"},
            "dark": {"bg": "#2b2b2b", "fg": "white", "button_bg": "#444", "button_fg": "white"}
        }

        # Initialize with Login Page
        self.show_login_page()

    def apply_theme(self, widget):
        """Applies the current theme to a given widget."""
        theme_colors = self.themes[self.theme]
        
        # Apply background color to all widgets
        widget.config(bg=theme_colors["bg"])
        
        for child in widget.winfo_children():
            # Apply background and foreground colors to supported widgets
            if isinstance(child, (tk.Label, tk.Button, tk.Entry)):
                child.config(bg=theme_colors["bg"], fg=theme_colors["fg"])
            elif isinstance(child, tk.Frame):
                # Recursively apply theme to frames
                self.apply_theme(child)

    def toggle_theme(self):
        """Switches between light and dark mode."""
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme(self)
        messagebox.showinfo("Theme Switched", f"Switched to {'Dark' if self.theme == 'dark' else 'Light'} Mode!")

    def show_login_page(self):
        self.clear_window()
        login_page = LoginPage(self)
        login_page.pack(fill="both", expand=True)
        self.apply_theme(login_page)

    def show_tracker_page(self):
        self.clear_window()
        tracker_page = TrackerPage(self)
        tracker_page.pack(fill="both", expand=True)
        self.apply_theme(tracker_page)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Widgets
        tk.Label(self, text="Login/Signup", font=("Arial", 16)).pack(pady=50)

        tk.Label(self, text="Username:").pack(anchor="w", padx=20)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(fill="x", padx=20)

        tk.Label(self, text="Password:").pack(anchor="w", padx=20)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(fill="x", padx=20)

        tk.Button(self, text="Login", command=self.login).pack(pady=5)
        signup_button = tk.Button(self, text="Sign Up", font=("Arial", 12), bg="#10b981", fg="white",
                                  relief="flat", width=10)
        signup_button.pack(pady=20, padx=10)

        # Theme Toggle Button
        tk.Button(self, text="Switch Theme", command=self.master.toggle_theme).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.master.users and self.master.users[username] == password:
            messagebox.showinfo("Success", "Login successful!")
            self.master.show_tracker_page()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.master.users:
            messagebox.showerror("Error", "Username already exists.")
        else:
            self.master.users[username] = password
            save_users(self.master.users)
            messagebox.showinfo("Success", "Signup successful!")

class TrackerPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Widgets
        tk.Label(self, text="Tracker", font=("Arial", 16)).pack(pady=10)

        self.start_button = tk.Button(self, text="Start", command=self.start_tracking)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop_tracking)
        self.stop_button.pack(pady=10)

        # Theme Toggle Button
        tk.Button(self, text="Switch Theme", command=self.master.toggle_theme).pack(pady=10)

    def start_tracking(self):
        messagebox.showinfo("Tracker", "Tracking started!")

    def stop_tracking(self):
        messagebox.showinfo("Tracker", "Tracking stopped!")

# Run the application
if __name__ == "__main__":
    app = TrackerApp()
    app.iconbitmap('logo2.ico')
    app.mainloop()

