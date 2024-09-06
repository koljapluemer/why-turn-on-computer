import webview
import os
import re
import json
from time import sleep

from appdirs import user_config_dir, user_data_dir

dir = os.path.dirname(__file__)

GOAL_NOTE = "🐑 I build the best learning tool possible"
OBS_DIR = "/home/b/MEGA/Obsidian/Zettelkasten/Thoughts"


# Arrays to store goals
goals = []
actionable_goals = []


def find_goals():
    # Start processing from the main file
    main_file_path = find_file_in_directory(GOAL_NOTE)
    print("main file path", main_file_path)
    if main_file_path:
        extract_goals(main_file_path)

    # Output the results
    print("Goals:", goals)
    print("Actionable Goals:", actionable_goals)

    return actionable_goals


# Function to extract goals from a file
def extract_goals(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regex pattern to find [[filename]] syntax
    matches = re.findall(r'\[\[([^\[\]]+)\]\]', content)

    # Track if the file has more goals to find
    found_goals = False

    for match in matches:
        if '🐑' in match:
            goal_path = find_file_in_directory(match)
            if goal_path and goal_path not in goals:
                goals.append(goal_path)
                found_goals = True
                # Recursively process the goal
                extract_goals(goal_path)

    # If no goals were found, mark as actionable
    if not found_goals and file_path not in actionable_goals:
        # save only the filename, not path
        actionable_goals.append(os.path.basename(file_path))

# Function to search for a file in the working directory
def find_file_in_directory(filename):
    for root, dirs, files in os.walk(OBS_DIR):
        for file in files:
            if file == f"{filename}.md":
                return os.path.join(root, file)
    return None



# Function to load current_goal
def getNextStep():
    config_dir = user_config_dir("goals")
    config_file = os.path.join(config_dir, "config.txt")
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as config:
            line = config.readline()
            return line.strip().split('=')[1]  # Get value after '='
    else:
        return None  # Return None if the config file doesn't exist



# Create a class to expose to JavaScript
class Api():
    def log(self, value):
        print(value)
    def openViewEditGoals(self):
        path = os.path.join(dir, 'goal_edit.html')
        with open(path, 'r') as file:
            html = file.read()
            window = webview.create_window("Edit Goals", html=html, js_api=Api())
            webview.start(window)


    # Function to save current_goal
    def setNextStep(self, current_goal):
        # Get platform-specific config directory
        config_dir = user_config_dir("goals")
        
        # Ensure the directory exists
        os.makedirs(config_dir, exist_ok=True)
        
        # File path for current_goal
        config_file = os.path.join(config_dir, "config.txt")
        
        # Save current_goal as a simple value in the config file
        with open(config_file, 'w') as config:
            config.write(f"current_goal={current_goal}\n")



def main():
    goals = find_goals()
    goals_as_json_string = json.dumps(goals)
    path = os.path.join(dir, 'main.html')
    with open (path, 'r') as file:
        html = file.read()
        html = html.replace("$NEXTSTEP", getNextStep())
        html = html.replace("$GOALS_AS_STRING", goals_as_json_string)
        window = webview.create_window("on program", html=html, js_api=Api(), on_top=True, frameless=False, width=1000, height=1, transparent=False, x = 150, y= 1300)
        webview.start(window)


if __name__ == '__main__':
    main()