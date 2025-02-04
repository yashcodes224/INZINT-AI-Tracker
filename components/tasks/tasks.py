import customtkinter as ctk
from components.tasks.task_form import TaskForm
from components.timer import TimerMixin

class TasksSection(ctk.CTkFrame, TimerMixin):
    def __init__(self, parent, app):
        ctk.CTkFrame.__init__(self, parent)
        TimerMixin.__init__(self, app)

        self.app = app  # Store app reference

        # Set background to white
        self.configure(fg_color="white")

        # Left (tasks) and Right (timer) sections
        self.left_frame = ctk.CTkFrame(self, fg_color="#f2f4f7", corner_radius=0)
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.left_frame.pack_propagate(False)

        self.show_tasks_view()

    def show_tasks_view(self):
        """Show the tasks list in the left section."""
        self.clear_left_frame()
        self._create_tasks_section()

    def _create_tasks_section(self):
        """Create the tasks section with header and tabs."""

        # Section Header
        header_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 5))

        header = ctk.CTkLabel(header_frame, text="My Tasks", font=("Roboto", 24, "bold"), text_color="black")
        header.pack(side="left")

        create_task_btn = ctk.CTkButton(
            header_frame,
            text="+ Create Task",
            fg_color="#f43f5e",
            text_color="white",
            hover_color="#e11d48",
            font=("Roboto", 14, "bold"),
            corner_radius=8,
            command=self.show_task_form
        )
        create_task_btn.pack(side="right", padx=10)

        # Task Tabs
        tab_view = ctk.CTkTabview(self.left_frame, fg_color="white", corner_radius=12)
        tab_view.pack(fill="both", expand=True, padx=5, pady=5)

        # Styling tabs
        tab_view._segmented_button.configure(
            fg_color="#B91C1C",
            selected_color="#f43f5e",
            unselected_color="#FCA5A5",
            text_color="white"
        )

        self.todo_tab = tab_view.add("To-Do")
        self.completed_tab = tab_view.add("Completed")

        self.render_tasks()

    def render_tasks(self):
        """Render all tasks in the To-Do and Completed tabs."""
        for tab in [self.todo_tab, self.completed_tab]:
            for widget in tab.winfo_children():
                widget.destroy()

        # Start rendering tasks **immediately below the tab** (no extra spacing)
        for task in self.app.task_data:
            parent_tab = self.todo_tab if not task.get("completed", False) else self.completed_tab

            task_frame = ctk.CTkFrame(
                parent_tab,
                fg_color="#FDE2E4",  # Task background highlighted
                corner_radius=12,
                border_width=1,  # Thin border around task
                border_color="#B91C1C"  # Darker red border
            )
            task_frame.pack(fill="x", pady=3, padx=8)

            # Task Layout (Compact & Balanced)
            task_container = ctk.CTkFrame(task_frame, fg_color="transparent")
            task_container.pack(fill="both", expand=True, padx=8, pady=5)

            # Radio button for task completion
            radio_var = ctk.StringVar(value="completed" if task["completed"] else "pending")
            task_radio = ctk.CTkRadioButton(
                task_container,
                text="",
                variable=radio_var,
                value="completed",
                fg_color="#f43f5e",
                command=lambda t=task: self.toggle_task_completion(t)
            )
            task_radio.pack(side="left", padx=5, pady=2)
            if task["completed"]:
                task_radio.select()

            # Task Info Section (Reduced Space Between Elements)
            task_info = ctk.CTkFrame(task_container, fg_color="transparent")
            task_info.pack(side="left", fill="x", expand=True, padx=8)

            task_name = ctk.CTkLabel(task_info, text=task["name"], font=("Roboto", 16, "bold"), text_color="#1E293B")
            task_name.pack(anchor="w", pady=1)

            project_name = ctk.CTkLabel(task_info, text=task["project"], font=("Roboto", 12), text_color="#64748B")
            project_name.pack(anchor="w", pady=1)

            # Timer & Actions Section
            action_frame = ctk.CTkFrame(task_container, fg_color="transparent")
            action_frame.pack(side="right", padx=5, pady=2)

            time_label = ctk.CTkLabel(action_frame, text=task["time"], font=("Roboto", 12), text_color="#475569")
            time_label.pack(side="left", padx=5)

            # Start/Stop Timer Button
            action_button = ctk.CTkButton(
                action_frame,
                text="▶ Start" if not task["running"] else "⏹ Stop",
                width=60,
                font=("Roboto", 12, "bold"),
                fg_color="#22C55E" if not task["running"] else "#DC2626",
                hover_color="#16A34A" if not task["running"] else "#B91C1C",
                corner_radius=8,
                command=lambda t=task: self.toggle_task_timer(t)
            )
            action_button.pack(side="left")

    def toggle_task_completion(self, task):
        """Mark a task as completed or incomplete."""
        task["completed"] = not task["completed"]
        self.render_tasks()

    def toggle_task_timer(self, task):
        """Start/Stop the timer for a task."""
        task["running"] = not task["running"]
        self.render_tasks()

    def show_task_form(self):
        """Show the Task Form in the left section."""
        self.clear_left_frame()
        TaskForm(self.left_frame, self.app, self.show_tasks_view).pack(fill="both", expand=True)

    def clear_left_frame(self):
        """Clear all widgets in the left frame."""
        for widget in self.left_frame.winfo_children():
            widget.destroy()