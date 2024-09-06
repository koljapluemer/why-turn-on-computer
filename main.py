import webview
import os

from time import sleep


dir = os.path.dirname(__file__)


import json
from appdirs import user_config_dir, user_data_dir



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

# Function to save goals_dict (the nested dictionary)
def save_goals_dict(goals_dict):
    # Get platform-specific data directory
    data_dir = user_data_dir("goals")
    
    # Ensure the directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # File path for goals_dict
    goals_file = os.path.join(data_dir, "goals.json")
    
    # Save the nested dictionary to goals.json
    with open(goals_file, 'w') as goals:
        json.dump(goals_dict, goals, indent=4)

# Function to load goals_dict
def load_goals_dict():
    data_dir = user_data_dir("goals")
    goals_file = os.path.join(data_dir, "goals.json")
    
    if os.path.exists(goals_file):
        with open(goals_file, 'r') as goals:
            return json.load(goals)
    else:
        return None  # Return None if the goals file doesn't exist



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
    path = os.path.join(dir, 'main.html')
    with open (path, 'r') as file:
        html = file.read()
        html = html.replace("$NEXTSTEP", getNextStep())
        window = webview.create_window("on program", html=html, js_api=Api(), on_top=True, frameless=False, width=1000, height=1, transparent=False, x = 150, y= 1300)
        webview.start(window)


if __name__ == '__main__':
    main()