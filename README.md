# Why Turn On Computer?

![screenshot](screenshot.png)

A little tkinter app running on autostart asking me why I turned on my computer, and in the end checks whether I did what I set out to do. In between, lives as a little mini-window on the bottom edge of my screen.

## Software

- A simple one-script python tkinter app (`main.py`)
- Can be built, but can also just be run

## Running it

- `uv run python main.py`
- to be really effective, put the script in OS's autostart
- on first run, you'll be prompted to set your purpose
- you can change your purpose anytime using the "Change Purpose" button

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