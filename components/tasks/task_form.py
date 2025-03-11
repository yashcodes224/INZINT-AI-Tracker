import customtkinter as ctk
import requests
import threading
from CTkMessagebox import CTkMessagebox
from components.tasks.task_form_style import LIGHT_THEME, DARK_THEME  # Import styles


# API Endpoint
API_PROFILE_URL = "https://o9bc4pbt8b.execute-api.ap-south-1.amazonaws.com/development/profile"

class TaskForm(ctk.CTkFrame):
    def __init__(self, parent, app, on_task_created, token):
        super().__init__(parent)
        self.app = app
        self.token = token
        self.on_task_created = on_task_created  

        self.apply_theme()
        self.configure(fg_color=self.theme["background"])

        # Header
        header = ctk.CTkLabel(
            self, 
            text="Create Task", 
            font=self.theme["header"]["font"], 
            text_color=self.theme["header"]["text_color"]
        )
        header.pack(anchor="w", padx=20, pady=(20, 15))

        # Task Name Field
        task_name_label = ctk.CTkLabel(
            self, 
            text="Task Name *", 
            font=self.theme["label"]["font"], 
            text_color=self.theme["label"]["text_color"]
        )
        task_name_label.pack(anchor="w", padx=20, pady=(10, 0))

        self.task_name_entry = ctk.CTkEntry(
            self,
            placeholder_text="Write task name...",
            width=self.theme["entry"]["width"],
            height=self.theme["entry"]["height"],
            fg_color=self.theme["entry"]["fg_color"],
            text_color=self.theme["entry"]["text_color"],
            border_width=self.theme["entry"]["border_width"],
            border_color=self.theme["entry"]["border_color"]
        )
        self.task_name_entry.pack(anchor="w", padx=20, pady=(5, 15))
        self.task_name_entry.bind("<FocusIn>", self.highlight_entry)
        self.task_name_entry.bind("<FocusOut>", self.reset_entry_border)

        # Project Dropdown
        project_label = ctk.CTkLabel(
            self, 
            text="Project *", 
            font=self.theme["label"]["font"], 
            text_color=self.theme["label"]["text_color"]
        )
        project_label.pack(anchor="w", padx=20, pady=(5, 0))

        # Default Placeholder for Dropdown
        self.project_option_menu = ctk.CTkOptionMenu(
            self,
            values=["Fetching projects..."],  # Default placeholder
            width=self.theme["dropdown"]["width"],
            height=self.theme["dropdown"]["height"],
            fg_color=self.theme["dropdown"]["fg_color"],
            text_color=self.theme["dropdown"]["text_color"],
            dropdown_fg_color=self.theme["dropdown"]["dropdown_fg_color"],
            dropdown_hover_color=self.theme["dropdown"]["dropdown_hover_color"],
            button_color=self.theme["dropdown"]["button_color"],
            button_hover_color=self.theme["dropdown"]["button_hover_color"],
            dropdown_text_color=self.theme["dropdown"]["dropdown_text_color"]
        )
        self.project_option_menu.pack(anchor="w", padx=20, pady=(5, 20))

        # Fetch projects asynchronously using profile API
        threading.Thread(target=self.fetch_profile, daemon=True).start()

        # Button Frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=30)

        # Cancel Button
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=self.theme["cancel_button"]["width"],
            height=self.theme["cancel_button"]["height"],
            fg_color=self.theme["cancel_button"]["fg_color"],
            text_color=self.theme["cancel_button"]["text_color"],
            border_width=self.theme["cancel_button"]["border_width"],
            border_color=self.theme["cancel_button"]["border_color"],
            hover_color=self.theme["cancel_button"]["hover_color"],
            font=self.theme["cancel_button"]["font"],
            corner_radius=self.theme["cancel_button"]["corner_radius"],
            command=self.cancel_task
        )
        cancel_button.pack(side="left", padx=10)

        # Create Button
        create_button = ctk.CTkButton(
            button_frame,
            text="Create",
            width=self.theme["create_button"]["width"],
            height=self.theme["create_button"]["height"],
            fg_color=self.theme["create_button"]["fg_color"],
            text_color=self.theme["create_button"]["text_color"],
            hover_color=self.theme["create_button"]["hover_color"],
            font=self.theme["create_button"]["font"],
            corner_radius=self.theme["create_button"]["corner_radius"],
            command=self.create_task
        )
        create_button.pack(side="left", padx=10)

    def apply_theme(self):
        """Apply the selected theme (Light or Dark)."""
        self.theme = LIGHT_THEME if self.app.current_theme == "Light" else DARK_THEME
        self.configure(fg_color=self.theme["background"])

    def fetch_profile(self):
        """Fetch user profile to get project IDs and then fetch projects by ID."""
        headers = {
            "Authorization": f"Bearer {self.app.token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(API_PROFILE_URL, headers=headers)
            print(f"Profile API Response: {response.status_code} - {response.text}")  # Debugging

            if response.status_code == 200:
                profile_data = response.json()

                if not isinstance(profile_data, dict):
                    print("Unexpected API response format:", profile_data)
                    return

                project_ids = profile_data.get("projects", [])  # Directly get list of project IDs

                if project_ids:
                    self.fetch_projects_by_id(project_ids)  # Fetch project details
                else:
                    self.project_option_menu.configure(values=["No Projects Assigned..."])
                    self.project_option_menu.set("No Projects Assigned...")
            else:
                print(f"Error fetching profile: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print("Error fetching profile:", e)


    def fetch_projects_by_id(self, project_ids):
        """Fetch project details using project IDs."""
        headers = {
            "Authorization": f"Bearer {self.app.token}",
            "Content-Type": "application/json"
        }

        project_names = []
        for project_id in project_ids:
            try:
                project_url = f"https://o9bc4pbt8b.execute-api.ap-south-1.amazonaws.com/development/projects/{project_id}"
                response = requests.get(project_url, headers=headers)

                print(f"Project API Response ({project_id}): {response.status_code} - {response.text}")  # Debugging

                if response.status_code == 200:
                    project_data = response.json()
                    project_names.append(project_data.get("name", "Unknown Project"))
                else:
                    print(f"Error fetching project {project_id}: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                print(f"Error fetching project {project_id}:", e)

        # Update dropdown with fetched project names
        if project_names:
            self.project_option_menu.configure(values=project_names)
            self.project_option_menu.set(project_names[0])
        else:
            self.project_option_menu.configure(values=["No Projects Assigned..."])
            self.project_option_menu.set("No Projects Assigned...")


    def highlight_entry(self, event):
        """Change border color when entry box is clicked."""
        self.task_name_entry.configure(border_color=self.theme["entry"]["focus_border_color"])

    def reset_entry_border(self, event):
        """Reset border color when focus is lost."""
        self.task_name_entry.configure(border_color=self.theme["entry"]["border_color"])

    def cancel_task(self):
        """Navigate back to the To-Do tab."""
        self.on_task_created()  

    def create_task(self):
        """Save the task and update the task list."""
        task_name = self.task_name_entry.get()
        project_name = self.project_option_menu.get()

        if not task_name.strip():
            CTkMessagebox(title="Error", message="Task name cannot be empty!", icon="cancel")
            return

        self.app.task_data.append({
            "name": task_name, 
            "project": project_name, 
            "time": "00:00", 
            "running": False, 
            "completed": False
        })

        self.on_task_created()  
