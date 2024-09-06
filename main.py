import webview
import os


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
        window = webview.create_window("Test", html=html, js_api=Api(), on_top=True, frameless=False, width=300, height=20, transparent=True)
        webview.start(window)


if __name__ == '__main__':
    main()