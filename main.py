import webview
import os


def custom_logic(window):
    window.toggle_fullscreen()
    window.evaluate_js('alert("Nice one brother")')


class Api():
  def log(self, value):
    print(value)

with open ('assets/main.html', 'r') as file:
    html = file.read()
    # window = webview.create_window('Woah dude!', html=html)
    window = webview.create_window("Test", html=html, js_api=Api())
    webview.start(window)
