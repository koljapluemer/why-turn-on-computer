import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import time
from datetime import datetime

from appdirs import user_config_dir, user_data_dir
import os
import json


# Data Model for storing task information
class Task:
    def __init__(self, goal="", estimated_time=0):
        self.goal = goal
        self.estimated_time = estimated_time
        self.start_time = None
        self.end_time = None
        self.result = None
        self.comment = ""

    def set_start_time(self):
        self.start_time = time.time()

    def set_end_time(self):
        self.end_time = time.time()

    def get_duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

    def save(self):
        # Prepare the data to be saved in NAME=VALUE format
        duration = self.get_duration()
        task_data = [
            f"goal={self.goal}",
            f"estimated_time={self.estimated_time}",
            f"result={self.result}",
            f"comment={self.comment}",
            f"duration={duration}",
            f"start_time={datetime.fromtimestamp(self.start_time).isoformat()}",
            f"end_time={datetime.fromtimestamp(self.end_time).isoformat()}"
        ]

        # Get the user data directory using appdirs
        app_name = "GoalTracker"
        app_author = "YourName"  # Adjust this if needed
        data_dir = user_data_dir(app_name, app_author)

        # Ensure the directory exists
        os.makedirs(data_dir, exist_ok=True)

        # Create a new text file with a timestamp in the filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file_path = os.path.join(data_dir, f'task_{timestamp}.txt')

        # Write each task data field as NAME=VALUE on a new line
        with open(log_file_path, 'w') as log_file:
            for line in task_data:
                log_file.write(f"{line}\n")

        print(f"Task data saved to {log_file_path}")

# Controller class to manage app flow
class TaskManager:
    def __init__(self, root):
        self.root = root
        self.task = Task()
        self.show_fullscreen_input_window()

    def show_fullscreen_input_window(self):
        fullscreen_window = tk.Toplevel(self.root)
        fullscreen_window.attributes("-fullscreen", True)
        fullscreen_window.attributes("-topmost", True)

        ttk.Label(fullscreen_window, text="Why did you turn on your computer?", font=("Arial", 24)).pack(pady=50)
        
        self.goal_input = ttk.Entry(fullscreen_window, font=("Arial", 20), width=50)
        self.goal_input.pack(pady=10)
        
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
        feedback_window.geometry("400x700")
        feedback_window.attributes("-topmost", True)

        ttk.Label(feedback_window, text="Goal Reached (0-10)", font=("Arial", 16)).pack(pady=20)
        self.result_input = ttk.Entry(feedback_window, font=("Arial", 14))
        self.result_input.pack(pady=10)

        ttk.Label(feedback_window, text="Comments", font=("Arial", 16)).pack(pady=20)
        self.comment_input = tk.Text(feedback_window, font=("Arial", 14), height=5)
        self.comment_input.pack(pady=10)

        submit_button = ttk.Button(feedback_window, text="Submit", command=self.on_submit)
        submit_button.pack(pady=20)

        self.feedback_window = feedback_window

    def on_submit(self):
        result = self.result_input.get()
        comment = self.comment_input.get("1.0", tk.END).strip()
        if result.isdigit() and 0 <= int(result) <= 10:
            self.task.result = int(result)
            self.task.comment = comment
            self.task.save()
            self.feedback_window.destroy()
            self.root.quit()

# Main function to run the app
def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    task_manager = TaskManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
