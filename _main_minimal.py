import webview
import os
import re
import json
from time import sleep
import random
from appdirs import user_config_dir, user_data_dir


dir = os.path.dirname(__file__)

start_window = None

class Api():
    def log(self, value):
        print(value)
    def set_goal(self, goal):
        config_dir = user_config_dir("goals")
        # Ensure the directory exists
        os.makedirs(config_dir, exist_ok=True)
        # File path for current_goal
        config_file = os.path.join(config_dir, "config.txt")
        # Save current_goal as a simple value in the config file
        with open(config_file, 'w') as config:
            config.write(f"current_goal={goal}\n")
        
        # close the window, and trigger open_goal_bar
        global start_window
        start_window.destroy()
        open_goal_bar()


def get_current_goal():
    config_dir = user_config_dir("goals")
    config_file = os.path.join(config_dir, "config.txt")
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as config:
            line = config.readline()
            return line.strip().split('=')[1]  # Get value after '='
    else:
        return None  # Return None if the config file doesn't exist


def open_goal_bar():
    path = os.path.join(dir, 'main.html')
    with open (path, 'r') as file:
        html = file.read()
        html = html.replace("$NEXTSTEP", get_current_goal())
        window = webview.create_window("on program", html=html, js_api=Api(), on_top=True, frameless=True, width=1200, height=10, transparent=False, x = 150, y= -10, resizable=False, easy_drag=False, min_size=(1200, 20)) #1300
        # webview.start(window)

def ask_for_goal():
    path = os.path.join(dir, 'ask_for_goal.html')
    # open full screen window
    with open (path, 'r') as file:
        html = file.read()
        window = webview.create_window("Ask For Goal", html=html, js_api=Api(), on_top=True, frameless=False, transparent=False,resizable=False, easy_drag=False, fullscreen=True)
        global start_window
        start_window = window
        webview.start(window)

def main():
    ask_for_goal()
    # open_goal_bar()





if __name__ == '__main__':
    main()