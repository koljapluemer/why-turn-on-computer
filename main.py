import webview
import os

from time import sleep

# Create a class to expose to JavaScript
class Api():
    def log(self, value):
        print(value)
    def openViewEditGoals(self):
        with open('assets/goal_edit.html', 'r') as file:
            html = file.read()
            window = webview.create_window("Edit Goals", html=html, js_api=Api())
            webview.start(window)



def main():
    with open ('assets/main.html', 'r') as file:
        html = file.read()
        # window = webview.create_window('Woah dude!', html=html)
        window = webview.create_window("on program", html=html, js_api=Api(), on_top=True, frameless=False, width=1000, height=1, transparent=False, x = 150, y= 1300)
        webview.start(window)


if __name__ == '__main__':
    main()