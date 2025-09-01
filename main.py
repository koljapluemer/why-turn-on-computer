import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime
import os
import subprocess

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_purpose():
    """Load purpose from purpose.txt file. Returns empty string if file not found."""
    try:
        purpose_path = os.path.join(SCRIPT_DIR, "purpose.txt")
        with open(purpose_path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

# Load purpose from text file
PURPOSE = load_purpose()

class Task:
    def __init__(self):
        self.reason = ""
        self.how_helps = ""
        self.start_time = None
        self.end_time = None
        self.goal_fulfilled = None
        self.actually_helped = None
        self.stay_on_goal = None
        self.comment = ""

    def set_start_time(self):
        self.start_time = time.time()

    def set_end_time(self):
        self.end_time = time.time()

    def get_duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

    def save_data(self):
        start_time = datetime.fromtimestamp(self.start_time).isoformat()
        duration = self.get_duration()
        
        task_data = [
            f"start_time={start_time}",
            f"reason={self.reason}",
            f"how_helps={self.how_helps}",
            f"duration={duration}",
            f"goal_fulfilled={self.goal_fulfilled}",
            f"actually_helped={self.actually_helped}",
            f"stay_on_goal={self.stay_on_goal}",
            f"comment={self.comment}",
            f"end_time={datetime.fromtimestamp(self.end_time).isoformat()}"
        ]

        data_dir = os.path.join(os.path.expanduser("~"), ".why_computer")
        os.makedirs(data_dir, exist_ok=True)
        
        log_file_path = os.path.join(data_dir, f'session_{start_time}.txt')
        
        with open(log_file_path, 'w') as log_file:
            for line in task_data:
                log_file.write(f"{line}\n")
        
        print(f"Session data saved to {log_file_path}")

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.task = Task()
        
        # Configure dark theme
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for dark theme
        style.configure(".", 
            background="#2b2b2b",
            foreground="#ffffff",
            fieldbackground="#3c3f41",
            selectbackground="#4b6eaf",
            selectforeground="#ffffff"
        )
        
        style.configure("TLabel", background="#2b2b2b", foreground="#ffffff")
        style.configure("TEntry", fieldbackground="#3c3f41", foreground="#ffffff")
        style.configure("TButton", background="#3c3f41", foreground="#ffffff", padding=5)
        style.configure("TFrame", background="#2b2b2b")
        style.configure("TRadiobutton", background="#2b2b2b", foreground="#ffffff")
        
        self.root.configure(bg="#2b2b2b")
        self.show_fullscreen_input_window()

    def show_fullscreen_input_window(self):
        fullscreen_window = tk.Toplevel(self.root)
        fullscreen_window.attributes("-fullscreen", True)
        fullscreen_window.attributes("-topmost", True)
        fullscreen_window.configure(bg="#2b2b2b")

        ttk.Label(fullscreen_window, text="Why did you turn on your computer?", font=("Arial", 24)).pack(pady=30)
        
        self.reason_input = ttk.Entry(fullscreen_window, font=("Arial", 20), width=60)
        self.reason_input.pack(pady=10)

        ttk.Label(fullscreen_window, text=f"How will this help with: {PURPOSE}?", font=("Arial", 18)).pack(pady=30)
        
        self.how_helps_input = ttk.Entry(fullscreen_window, font=("Arial", 16), width=60)
        self.how_helps_input.pack(pady=10)
        
        confirm_button = ttk.Button(fullscreen_window, text="Confirm", command=self.on_confirm)
        confirm_button.pack(pady=30)

        self.fullscreen_window = fullscreen_window

    def on_confirm(self):
        reason = self.reason_input.get().strip()
        how_helps = self.how_helps_input.get().strip()
        if reason and how_helps:
            self.task.reason = reason
            self.task.how_helps = how_helps
            self.task.set_start_time()
            
            self.fullscreen_window.destroy()
            self.show_task_window()

    def show_task_window(self):
        task_window = tk.Toplevel(self.root)
        task_window.overrideredirect(True)
        task_window.geometry(f"600x25+100+{self.root.winfo_screenheight()-25}")
        task_window.attributes("-topmost", True)
        task_window.configure(bg="#2b2b2b")

        content_frame = ttk.Frame(task_window, padding=(5, 2, 5, 2))
        content_frame.pack(fill="both", expand=True)

        reason_label = ttk.Label(content_frame, text=f"{self.task.reason}", font=("Arial", 10))
        reason_label.pack(side="left", padx=(2, 5))

        finish_button = ttk.Button(content_frame, text="Finish", command=self.on_finish)
        finish_button.pack(side="right", padx=(5, 2))

        self.task_window = task_window

    def on_finish(self):
        self.task.set_end_time()
        self.task_window.destroy()
        self.show_feedback_window()

    def show_feedback_window(self):
        feedback_window = tk.Toplevel(self.root)
        feedback_window.title("Session Feedback")
        feedback_window.attributes("-fullscreen", True)
        feedback_window.attributes("-topmost", True)
        feedback_window.configure(bg="#2b2b2b")

        main_frame = ttk.Frame(feedback_window, padding="40")
        main_frame.pack(expand=True, fill="both")

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(expand=True)

        # Show what they did
        ttk.Label(content_frame, text="What you did:", font=("Arial", 18, "bold")).pack(pady=(0, 5))
        ttk.Label(content_frame, text=self.task.reason, font=("Arial", 16)).pack(pady=(0, 20))
        
        # Show how it was supposed to help
        ttk.Label(content_frame, text="How this was supposed to help with purpose:", font=("Arial", 18, "bold")).pack(pady=(0, 5))
        ttk.Label(content_frame, text=self.task.how_helps, font=("Arial", 16)).pack(pady=(0, 30))

        # Goal fulfilled Likert scale
        ttk.Label(content_frame, text="Was your goal fulfilled?", font=("Arial", 18)).pack(pady=(0, 10))
        goal_frame = ttk.Frame(content_frame)
        goal_frame.pack(pady=(0, 20))
        
        ttk.Label(goal_frame, text="Not at all", font=("Arial", 12)).pack(side="left")
        self.goal_fulfilled = tk.IntVar(value=3)
        for i in range(1, 6):
            ttk.Radiobutton(goal_frame, text=str(i), variable=self.goal_fulfilled, value=i).pack(side="left", padx=5)
        ttk.Label(goal_frame, text="Very much", font=("Arial", 12)).pack(side="left")

        # Actually helped Likert scale
        ttk.Label(content_frame, text="Did this actually help with your purpose?", font=("Arial", 18)).pack(pady=(20, 10))
        help_frame = ttk.Frame(content_frame)
        help_frame.pack(pady=(0, 30))
        
        ttk.Label(help_frame, text="Not at all", font=("Arial", 12)).pack(side="left")
        self.actually_helped = tk.IntVar(value=3)
        for i in range(1, 6):
            ttk.Radiobutton(help_frame, text=str(i), variable=self.actually_helped, value=i).pack(side="left", padx=5)
        ttk.Label(help_frame, text="Very much", font=("Arial", 12)).pack(side="left")

        # Stay on goal Likert scale
        ttk.Label(content_frame, text="Did you stay on the goal?", font=("Arial", 18)).pack(pady=(20, 10))
        stay_on_goal_frame = ttk.Frame(content_frame)
        stay_on_goal_frame.pack(pady=(0, 20))
        
        ttk.Label(stay_on_goal_frame, text="Not at all", font=("Arial", 12)).pack(side="left")
        self.stay_on_goal = tk.IntVar(value=3)
        for i in range(1, 6):
            ttk.Radiobutton(stay_on_goal_frame, text=str(i), variable=self.stay_on_goal, value=i).pack(side="left", padx=5)
        ttk.Label(stay_on_goal_frame, text="Very much", font=("Arial", 12)).pack(side="left")

        # Comment field
        ttk.Label(content_frame, text="Additional comments (optional):", font=("Arial", 18)).pack(pady=(20, 10))
        comment_frame = ttk.Frame(content_frame)
        comment_frame.pack(pady=(0, 30), fill="x")
        
        self.comment_text = tk.Text(comment_frame, font=("Arial", 12), height=4, width=80, 
                                   bg="#3c3f41", fg="#ffffff", insertbackground="#ffffff")
        self.comment_text.pack(fill="x")

        # Buttons
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=30)

        ttk.Button(button_frame, text="Nevermind", command=self.on_nevermind).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Save", command=self.on_save).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Save and Shutdown", command=self.on_save_shutdown).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Save and Shutdown +5", command=self.on_save_shutdown_5).pack(side="left", padx=10)

        self.feedback_window = feedback_window

    def on_save(self):
        self.task.goal_fulfilled = self.goal_fulfilled.get()
        self.task.actually_helped = self.actually_helped.get()
        self.task.stay_on_goal = self.stay_on_goal.get()
        self.task.comment = self.comment_text.get("1.0", tk.END).strip()
        self.task.save_data()
        self.feedback_window.destroy()
        self.root.quit()

    def on_save_shutdown(self):
        self.on_save()
        subprocess.run(["shutdown", "-h", "now"])

    def on_save_shutdown_5(self):
        self.on_save()
        subprocess.run(["shutdown", "-h", "+5"])

    def on_nevermind(self):
        self.feedback_window.destroy()
        self.show_task_window()

def main():
    root = tk.Tk()
    root.withdraw()
    task_manager = TaskManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()