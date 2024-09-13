import webview
import os
import re
import json
from time import sleep
import random
from appdirs import user_config_dir, user_data_dir


dir = os.path.dirname(__file__)

class Api():
    def log(self, value):
        print(value)

def get_current_goal():
    config_dir = user_config_dir("goals")
    config_file = os.path.join(config_dir, "config.txt")
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as config:
            line = config.readline()
            return line.strip().split('=')[1]  # Get value after '='
    else:
        return None  # Return None if the config file doesn't exist

def main():
    path = os.path.join(dir, 'main.html')
    with open (path, 'r') as file:
        html = file.read()
        html = html.replace("$NEXTSTEP", get_current_goal())
        window = webview.create_window("on program", html=html, js_api=Api(), on_top=True, frameless=True, width=1200, height=10, transparent=False, x = 150, y= -10, resizable=False, easy_drag=False, min_size=(1200, 20)) #1300
        webview.start(window)


if __name__ == '__main__':
    main()