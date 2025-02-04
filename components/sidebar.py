# import customtkinter as ctk

# class Sidebar(ctk.CTkFrame):
#     def __init__(self, parent, navigation_handler):
#         super().__init__(parent, width=50, corner_radius=0)

#         self.nav_handler = navigation_handler
#         self.initialize_ui()

#     def initialize_ui(self):
#         # User Avatar
#         avatar = ctk.CTkLabel(self, text="👤 User", font=("Roboto", 18, "bold"))
#         avatar.pack(pady=5)

#         # Navigation Buttons
#         tasks_btn = ctk.CTkButton(self, text="Tasks", command=lambda: self.nav_handler("tasks"))
#         tasks_btn.pack(pady=5)

#         settings_btn = ctk.CTkButton(self, text="Settings", command=lambda: self.nav_handler("settings"))
#         settings_btn.pack(pady=5)
