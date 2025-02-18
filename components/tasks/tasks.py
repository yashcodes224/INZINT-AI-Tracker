import customtkinter as ctk
from components.tasks.task_form import TaskForm
from components.timer.timer import TimerMixin
from components.tasks.task_style import LIGHT_THEME, DARK_THEME  # Import both themes

class TasksSection(ctk.CTkFrame, TimerMixin):
    def __init__(self, parent, app):
        ctk.CTkFrame.__init__(self, parent)
        TimerMixin.__init__(self, app)

        self.app = app  # Store app reference

        # Apply the correct theme dynamically
        self.apply_theme()

        # Left (tasks) section
        self.left_frame = ctk.CTkFrame(self, fg_color=self.theme["left_frame"], corner_radius=0)
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.left_frame.pack_propagate(False)

        self.show_tasks_view()

    def apply_theme(self):
        """Apply the selected theme (Light or Dark)."""
        self.theme = LIGHT_THEME if self.app.current_theme == "Light" else DARK_THEME
        self.configure(fg_color=self.theme["background"])

    def show_tasks_view(self):
        """Show the tasks list in the left section."""
        self.clear_left_frame()
        self._create_tasks_section()

    def _create_tasks_section(self):
        """Create the tasks section with header and tabs."""

        # Section Header
        header_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 5))

        header = ctk.CTkLabel(
            header_frame,
            text="My Tasks",
            font=("Roboto", 24, "bold"),
            text_color=self.theme["header_text"]
        )
        header.pack(side="left")

        create_task_btn = ctk.CTkButton(
            header_frame,
            text="+ Create Task",
            fg_color=self.theme["create_task_btn"]["fg_color"],
            text_color=self.theme["create_task_btn"]["text_color"],
            hover_color=self.theme["create_task_btn"]["hover_color"],
            font=("Roboto", 14, "bold"),
            corner_radius=8,
            command=self.show_task_form
        )
        create_task_btn.pack(side="right", padx=10)

        # Task Tabs
        tab_view = ctk.CTkTabview(
            self.left_frame,
            fg_color=self.theme["tab_view"]["fg_color"],
            corner_radius=12
        )
        tab_view.pack(fill="both", expand=True, padx=5, pady=5)

        # Styling tabs
        tab_view._segmented_button.configure(
            fg_color=self.theme["tab_view"]["border_color"],
            selected_color=self.theme["tab_view"]["selected_color"],
            unselected_color=self.theme["tab_view"]["unselected_color"],
            text_color=self.theme["tab_view"]["text_color"]
        )

        self.todo_tab = tab_view.add("To-Do")
        self.completed_tab = tab_view.add("Completed")

        self.render_tasks()

    def render_tasks(self):
        """Render all tasks in the To-Do and Completed tabs."""
        for tab in [self.todo_tab, self.completed_tab]:
            for widget in tab.winfo_children():
                widget.destroy()

        for task in self.app.task_data:
            parent_tab = self.todo_tab if not task.get("completed", False) else self.completed_tab

            task_frame = ctk.CTkFrame(
                parent_tab,
                fg_color=self.theme["task_card"]["bg_color"],
                corner_radius=12,
                border_width=1,
                border_color=self.theme["task_card"]["border_color"]
            )
            task_frame.pack(fill="x", pady=3, padx=8)

            # ✅ Task Container (Expands Properly)
            task_container = ctk.CTkFrame(task_frame, fg_color="transparent")
            task_container.pack(fill="x", expand=True, padx=5, pady=5)
            task_container.grid_columnconfigure(1, weight=1)  # ✅ Allow text section to expand
            task_container.grid_columnconfigure(2, weight=0)  # ✅ Fix alignment of time on the right

            # ✅ Adjusted Radio Button (Reduced Space)
            radio_var = ctk.StringVar(value="completed" if task["completed"] else "pending")
            task_radio = ctk.CTkRadioButton(
                task_container,
                text="",
                variable=radio_var,
                value="completed",
                fg_color=self.theme["radio_button"]["fg_color"],
                command=lambda t=task: self.toggle_task_completion(t),
                width=5, height=5  # ✅ Make button smaller
            )
            task_radio.grid(row=0, column=0, padx=(8, 2), pady=2, sticky="w")  # ✅ Reduced padding

            if task["completed"]:
                task_radio.select()

            # ✅ Task Info Section (Expands Fully)
            task_info = ctk.CTkFrame(task_container, fg_color="transparent")
            task_info.grid(row=0, column=1, sticky="ew", padx=(2, 5))  # ✅ Reduced left padding

            # ✅ Task Name (No Extra Space)
            task_name = ctk.CTkLabel(
                task_info,
                text=task["name"],
                font=("Roboto", 16, "bold"),
                text_color=self.theme["task_card"]["text_color"],
                anchor="w"
            )
            task_name.pack(anchor="w", pady=1)

            # ✅ Project Name (Now Fully Visible)
            project_name = ctk.CTkLabel(
                task_info,
                text=task["project"],
                font=("Roboto", 12),
                text_color=self.theme["task_card"]["subtext_color"],
                wraplength=200,  # ✅ Prevent text from cutting off
                anchor="w",
                justify="left"
            )
            project_name.pack(anchor="w", pady=1)

            # ✅ Task Time (Right-Aligned)
            task_time = ctk.CTkLabel(
                task_container,
                text=task["time"],
                font=("Roboto", 12, "bold"),
                text_color=self.theme["task_card"]["time_color"],
                anchor="e"  # ✅ Align to the right
            )
            task_time.grid(row=0, column=2, padx=(5, 8), sticky="e")  # ✅ Proper alignment on the right

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
