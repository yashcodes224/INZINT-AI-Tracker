import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

class TaskForm(ctk.CTkFrame):
    def __init__(self, parent, app, on_task_created):
        super().__init__(parent)
        self.app = app
        self.on_task_created = on_task_created  # Callback for when a task is created

        self.configure(fg_color="#f2f4f7", corner_radius=0)  

        # Header
        header = ctk.CTkLabel(self, text="Create Task", font=("Roboto", 22, "bold"), text_color="#1E293B")
        header.pack(anchor="w", padx=20, pady=(20, 15))

        # Task Name Field
        task_name_label = ctk.CTkLabel(self, text="Task Name *", font=("Roboto", 14), text_color="#1E293B")
        task_name_label.pack(anchor="w", padx=20, pady=(10, 0))

        self.task_name_entry = ctk.CTkEntry(
            self, 
            placeholder_text="Write task name...", 
            width=320,  # Uniform width
            height=40,  # Matching height
            fg_color="white", 
            text_color="black",
            border_width=2,  # Thicker border for focus effect
            border_color="#D1D5DB"
        )
        self.task_name_entry.pack(anchor="w", padx=20, pady=(5, 15))
        self.task_name_entry.bind("<FocusIn>", self.highlight_entry)
        self.task_name_entry.bind("<FocusOut>", self.reset_entry_border)

        # Project Dropdown
        project_label = ctk.CTkLabel(self, text="Project *", font=("Roboto", 14), text_color="#1E293B")
        project_label.pack(anchor="w", padx=20, pady=(5, 0))

        self.project_option_menu = ctk.CTkOptionMenu(
            self, 
            values=["Inhouse AI Tracker", "Project X", "Other"], 
            width=320,  # Same width
            height=40,  # Matching height
            fg_color="white", 
            text_color="black",
            dropdown_fg_color="white",
            dropdown_hover_color="#f2f4f7",
            button_color="#f43f5e",  # Button color matches the theme
            button_hover_color="#e11d48"
        )
        self.project_option_menu.pack(anchor="w", padx=20, pady=(5, 20))

        # Apply red border effect on dropdown when clicked
        self.project_option_menu.bind("<FocusIn>", self.highlight_dropdown)
        self.project_option_menu.bind("<FocusOut>", self.reset_dropdown_border)

        # Button Frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=30)  # Increased spacing for a cleaner look

        # Cancel Button
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=150,
            height=40,
            fg_color="white",
            text_color="black",
            border_width=1,  # Light border for a cleaner look
            border_color="#D1D5DB",
            hover_color="#E2E8F0",
            font=("Roboto", 14, "bold"),
            corner_radius=8,
            command=self.cancel_task
        )
        cancel_button.pack(side="left", padx=10)

        # Create Button
        create_button = ctk.CTkButton(
            button_frame,
            text="Create",
            width=150,
            height=40,
            fg_color="#f43f5e",
            text_color="white",
            hover_color="#e11d48",
            font=("Roboto", 14, "bold"),
            corner_radius=8,
            command=self.create_task
        )
        create_button.pack(side="left", padx=10)

    def highlight_entry(self, event):
        """Change border color to red when the entry box is clicked."""
        self.task_name_entry.configure(border_color="#f43f5e")

    def reset_entry_border(self, event):
        """Reset border color when focus is lost."""
        self.task_name_entry.configure(border_color="#D1D5DB")

    def highlight_dropdown(self, event):
        """Change dropdown border color to red when clicked."""
        self.project_option_menu.configure(button_color="#f43f5e")

    def reset_dropdown_border(self, event):
        """Reset dropdown border color when focus is lost."""
        self.project_option_menu.configure(button_color="#D1D5DB")

    def cancel_task(self):
        """Navigate back to the To-Do tab."""
        self.on_task_created()  # Simply close the form

    def create_task(self):
        """Save the task and update the task list."""
        task_name = self.task_name_entry.get()
        project_name = self.project_option_menu.get()

        # Basic validation
        if not task_name.strip():
            CTkMessagebox(title="Error", message="Task name cannot be empty!", icon="cancel")
            return

        # Add the task to the task list
        self.app.task_data.append({
            "name": task_name, 
            "project": project_name, 
            "time": "00:00", 
            "running": False, 
            "completed": False
        })

        # Navigate back to the To-Do tab
        self.on_task_created()
