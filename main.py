import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import time
from datetime import datetime

from appdirs import user_config_dir, user_data_dir
import os
import json

import re

# Data Model for storing task information
class Task:
    def __init__(self, goal="", estimated_time=0, larger_goal="", hypothesis="", will_program=False, public_facing=False):
        self.goal = goal
        self.larger_goal = larger_goal
        self.estimated_time = estimated_time
        self.start_time = None
        self.end_time = None
        self.result = None
        self.comment = ""
        self.hypothesis = hypothesis
        self.will_program = will_program
        self.public_facing = public_facing
        # Programming-specific fields
        self.logged_in_obs = False
        self.drafted_outline = False
        self.tracked_issues = False
        self.changes_documented = False
        self.test_covered = False
        self.refactored = False
        self.screenshots_updated = False
        self.wrapped_in_story = False
        # Public-facing specific fields
        self.communication_done = False

    def set_start_time(self):
        self.start_time = time.time()

    def set_end_time(self):
        self.end_time = time.time()

    def get_duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

    def save_at_beginning(self):
        # Prepare the data to be saved in NAME=VALUE format
        duration = self.get_duration()
        start_time = datetime.fromtimestamp(self.start_time).isoformat()
        task_data = [
            f"goal={self.goal}",
            f"larger_goal={self.larger_goal}",
            f"hypothesis={self.hypothesis}",
            f"estimated_time={self.estimated_time}",
            f"start_time={start_time}",
            f"will_program={self.will_program}",
            f"public_facing={self.public_facing}",
        ]

        # Get the user data directory using appdirs
        app_name = "GoalTracker"
        app_author = "Kolja Sam"  # Adjust this if needed
        data_dir = user_data_dir(app_name, app_author)

        # Ensure the directory exists
        os.makedirs(data_dir, exist_ok=True)

        # Create a new text file with a timestamp in the filename
        log_file_path = os.path.join(data_dir, f'goal_{start_time}.txt')

        # Write each task data field as NAME=VALUE on a new line
        with open(log_file_path, 'w') as log_file:
            for line in task_data:
                log_file.write(f"{line}\n")

        print(f"Task data saved to {log_file_path}")

    def save_at_end(self):
        # Prepare the data to be saved in NAME=VALUE format
        duration = self.get_duration()
        start_time = datetime.fromtimestamp(self.start_time).isoformat()

        task_data = [
            f"result={self.result}",
            f"comment={self.comment}",
            f"duration={duration}",
            f"end_time={datetime.fromtimestamp(self.end_time).isoformat()}"
        ]

        # Add programming-specific data if applicable
        if self.will_program:
            task_data.extend([
                f"logged_in_obs={self.logged_in_obs}",
                f"drafted_outline={self.drafted_outline}",
                f"tracked_issues={self.tracked_issues}",
                f"changes_documented={self.changes_documented}",
                f"test_covered={self.test_covered}",
                f"refactored={self.refactored}",
                f"screenshots_updated={self.screenshots_updated}",
                f"wrapped_in_story={self.wrapped_in_story}"
            ])

        # Add public-facing specific data if applicable
        if self.public_facing:
            task_data.extend([
                f"communication_done={self.communication_done}"
            ])

        # Get the user data directory using appdirs
        app_name = "GoalTracker"
        app_author = "Kolja Sam"  # Adjust this if needed
        data_dir = user_data_dir(app_name, app_author)

        # Ensure the directory exists
        os.makedirs(data_dir, exist_ok=True)

        log_file_path = os.path.join(data_dir, f'goal_{start_time}.txt')

        # Write each task data field as NAME=VALUE on a new line
        with open(log_file_path, 'a') as log_file:
            for line in task_data:
                log_file.write(f"{line}\n")

        print(f"Task data saved to {log_file_path}")

# Controller class to manage app flow
class TaskManager:
    def __init__(self, root):
        self.root = root
        self.task = Task()
        
        # Create styles for larger widgets
        style = ttk.Style()
        style.configure("Large.TCheckbutton", font=("Arial", 14))
        style.configure("Large.TButton", font=("Arial", 14))
        
        self.show_fullscreen_input_window()

    def show_fullscreen_input_window(self):
        fullscreen_window = tk.Toplevel(self.root)
        fullscreen_window.attributes("-fullscreen", True)
        fullscreen_window.attributes("-topmost", True)

        ttk.Label(fullscreen_window, text="Why did you turn on your computer?", font=("Arial", 24)).pack(pady=50)
        
        self.goal_input = ttk.Entry(fullscreen_window, font=("Arial", 20), width=50)
        self.goal_input.pack(pady=10)

        # larger goal
        # read goals directly from goals.txt
        try:
            with open("goals.txt", "r") as f:
                larger_goals = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            larger_goals = ["No goals defined"]
        
        self.larger_goal = tk.StringVar()
        self.larger_goal.set(larger_goals[0] if larger_goals else "No goals defined")
        larger_goal_menu = ttk.OptionMenu(fullscreen_window, self.larger_goal, larger_goals[0] if larger_goals else "No goals defined", *larger_goals)
        larger_goal_menu.pack(pady=10)

        # will program checkbox
        self.will_program_var = tk.BooleanVar(value=False)
        will_program_checkbox = ttk.Checkbutton(fullscreen_window, text="Will program?", variable=self.will_program_var)
        will_program_checkbox.pack(pady=10)

        # public facing checkbox
        self.public_facing_var = tk.BooleanVar(value=False)
        public_facing_checkbox = ttk.Checkbutton(fullscreen_window, text="Public-facing?", variable=self.public_facing_var)
        public_facing_checkbox.pack(pady=10)

        # hypothesis (another simple text input)
        ttk.Label(fullscreen_window, text="Hypothesis", font=("Arial", 18)).pack(pady=20)
        self.hypothesis_input = ttk.Entry(fullscreen_window, font=("Arial", 16), width=50)
        self.hypothesis_input.pack(pady=10)


        # time needed
        
        ttk.Label(fullscreen_window, text="Estimated time needed (minutes)", font=("Arial", 18)).pack(pady=20)
        
        self.time_input = ttk.Entry(fullscreen_window, font=("Arial", 16), width=10)
        self.time_input.pack(pady=10)
        
        confirm_button = ttk.Button(fullscreen_window, text="Confirm", command=self.on_confirm)
        confirm_button.pack(pady=20)

        self.fullscreen_window = fullscreen_window

    def on_confirm(self):
        goal = self.goal_input.get()
        estimated_time = self.time_input.get()
        if goal and estimated_time.isdigit():
            self.task.goal = goal
            self.task.estimated_time = int(estimated_time)
            self.task.set_start_time()
            self.task.larger_goal = self.larger_goal.get()
            self.task.hypothesis = self.hypothesis_input.get()
            self.task.will_program = self.will_program_var.get()
            self.task.public_facing = self.public_facing_var.get()
            self.task.save_at_beginning()

            self.fullscreen_window.destroy()
            self.show_task_window()

    def show_task_window(self):
        task_window = tk.Toplevel(self.root)
        task_window.overrideredirect(True)  # Frameless
        task_window.geometry(f"500x20+100+{self.root.winfo_screenheight()-20}")  # Small height of 15px
        task_window.attributes("-topmost", True)

        # Frame to hold the content with no margins
        content_frame = ttk.Frame(task_window, padding=(0, 0, 0, 0))
        content_frame.pack(fill="both", expand=True)

        goal_label = ttk.Label(content_frame, text=f"{self.task.goal}", font=("Arial", 10))  # Smaller font
        goal_label.pack(side="left", padx=(2, 5), pady=0)  # Minimal padding

        finish_button = ttk.Button(content_frame, text="Finish", command=self.on_finish)
        finish_button.pack(side="right", padx=(5, 2), pady=0)  # Minimal padding

        self.task_window = task_window

    def on_finish(self):
        self.task.set_end_time()
        self.task_window.destroy()
        self.show_feedback_window()

    def show_feedback_window(self):
        feedback_window = tk.Toplevel(self.root)
        feedback_window.title("Task Feedback")
        feedback_window.attributes("-fullscreen", True)
        feedback_window.attributes("-topmost", True)

        # Main container frame
        main_frame = ttk.Frame(feedback_window, padding="20")
        main_frame.pack(expand=True, fill="both")

        # Content frame with max width
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(expand=True)

        ttk.Label(content_frame, text="Goal Reached (0-10)", font=("Arial", 18)).pack(pady=15)
        self.result_input = ttk.Entry(content_frame, font=("Arial", 16), width=10)
        self.result_input.pack(pady=5)

        ttk.Label(content_frame, text="Comments", font=("Arial", 18)).pack(pady=15)
        self.comment_input = tk.Text(content_frame, font=("Arial", 16), height=4, width=50)
        self.comment_input.pack(pady=5)

        # Add time information
        time_frame = ttk.Frame(content_frame)
        time_frame.pack(pady=10)
        
        # Estimated time
        ttk.Label(time_frame, text=f"Estimated: {self.task.estimated_time}m", 
                 font=("Arial", 16)).pack(side="left", padx=10)
        
        # Actual time taken
        duration = self.task.get_duration()
        if duration:
            minutes = int(duration / 60)
            seconds = int(duration % 60)
            time_taken = f"{minutes}m {seconds}s"
            ttk.Label(time_frame, text=f"Actual: {time_taken}", 
                     font=("Arial", 16)).pack(side="left", padx=10)

        # Add programming-specific checkboxes if applicable
        if self.task.will_program:
            ttk.Label(content_frame, text="Programming Tasks", font=("Arial", 18)).pack(pady=15)
            
            # Create a frame for checkboxes with left alignment
            checkbox_frame = ttk.Frame(content_frame)
            checkbox_frame.pack(fill="x", padx=20)
            
            self.logged_in_obs_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(checkbox_frame, text="Relevant learnings, snippets and log in Obs", 
                          variable=self.logged_in_obs_var, style="Large.TCheckbutton").pack(anchor="w", pady=5)
            
            self.drafted_outline_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(checkbox_frame, text="Drafted speculative outline", 
                          variable=self.drafted_outline_var, style="Large.TCheckbutton").pack(anchor="w", pady=5)
            
            self.tracked_issues_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(checkbox_frame, text="Emerging issues tracked in gh", 
                          variable=self.tracked_issues_var, style="Large.TCheckbutton").pack(anchor="w", pady=5)
            
            self.changes_documented_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(checkbox_frame, text="Changes indicated in .md in project", 
                          variable=self.changes_documented_var, style="Large.TCheckbutton").pack(anchor="w", pady=5)
            
            self.test_covered_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(checkbox_frame, text="Test-covered", 
                          variable=self.test_covered_var, style="Large.TCheckbutton").pack(anchor="w", pady=5)

            self.refactored_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(checkbox_frame, text="Refactored", 
                          variable=self.refactored_var, style="Large.TCheckbutton").pack(anchor="w", pady=5)

            self.screenshots_updated_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(checkbox_frame, text="New state reflected in screenshots", 
                          variable=self.screenshots_updated_var, style="Large.TCheckbutton").pack(anchor="w", pady=5)

            self.wrapped_in_story_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(checkbox_frame, text="Wrapped in user story", 
                          variable=self.wrapped_in_story_var, style="Large.TCheckbutton").pack(anchor="w", pady=5)

        # Add public-facing specific checkboxes if applicable
        if self.task.public_facing:
            ttk.Label(content_frame, text="Public-facing Tasks", font=("Arial", 18)).pack(pady=15)
            
            # Create a frame for checkboxes with left alignment
            public_checkbox_frame = ttk.Frame(content_frame)
            public_checkbox_frame.pack(fill="x", padx=20)
            
            self.communication_done_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(public_checkbox_frame, text="Communication done or scheduled", 
                          variable=self.communication_done_var, style="Large.TCheckbutton").pack(anchor="w", pady=5)

        # Button frame for better organization
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20)

        submit_button = ttk.Button(button_frame, text="Submit", command=self.on_submit, style="Large.TButton")
        submit_button.pack(side="left", padx=10)

        nevermind_button = ttk.Button(button_frame, text="Nevermind", command=self.on_nevermind, style="Large.TButton")
        nevermind_button.pack(side="left", padx=10)

        self.feedback_window = feedback_window

    def on_submit(self):
        result = self.result_input.get()
        comment = self.comment_input.get("1.0", tk.END).strip()
        if result.isdigit() and 0 <= int(result) <= 10:
            self.task.result = int(result)
            self.task.comment = comment
            
            # Save programming-specific data if applicable
            if self.task.will_program:
                self.task.logged_in_obs = self.logged_in_obs_var.get()
                self.task.drafted_outline = self.drafted_outline_var.get()
                self.task.tracked_issues = self.tracked_issues_var.get()
                self.task.changes_documented = self.changes_documented_var.get()
                self.task.test_covered = self.test_covered_var.get()
                self.task.refactored = self.refactored_var.get()
                self.task.screenshots_updated = self.screenshots_updated_var.get()
                self.task.wrapped_in_story = self.wrapped_in_story_var.get()
            
            # Save public-facing specific data if applicable
            if self.task.public_facing:
                self.task.communication_done = self.communication_done_var.get()
            
            self.task.save_at_end()
            self.feedback_window.destroy()
            self.root.quit()

    def on_nevermind(self):
        self.feedback_window.destroy()
        self.show_task_window()

# Main function to run the app
def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    task_manager = TaskManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
