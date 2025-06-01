# Why Turn On Computer?

![screenshot](screenshot.png)

A little tkinter app running on autostart asking me why I turned on my computer, and in the end checks whether I did what I set out to do. In between, lives as a little mini-window on the bottom edge of my screen.

## Running it

- default python app. make a `venv`, install reqs, run `main.py`.
- to be really effective, put the script (e.g. `python3 ~/GITHUB/why-turn-on-computer/main.py`) in OS's autostart
- create a `goals.json` file in the project directory with your goal categories and their associated checkboxes

## Configuration

### goals.json
JSON file defining goal categories and their associated checkboxes. Structure:
```json
{
    "Category Name": [
        "Checkbox 1",
        "Checkbox 2"
    ]
}
```

## Documentation


- whole thing is mostly controlled by `