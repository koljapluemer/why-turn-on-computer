"""Configuration management for Why Turn On Computer."""
import json
import os
import appdirs

APP_NAME = "why-turn-on-computer"
APP_AUTHOR = "KoljaSam"

# Default values
DEFAULT_QUESTION_TEXT = "Why did you turn on your computer?"
DEFAULT_EVALUATION_QUESTIONS = [
    "Did you accomplish what you set out to do?",
    "Did you stay focused on your goal?"
]


def get_config_dir():
    """Get the config directory using appdirs."""
    config_dir = appdirs.user_config_dir(APP_NAME, APP_AUTHOR)
    os.makedirs(config_dir, exist_ok=True)
    return config_dir


def get_config_file_path():
    """Get the full path to the config file."""
    return os.path.join(get_config_dir(), "config.json")


def load_config():
    """Load config from JSON file. Returns dict with config or empty dict if not found."""
    try:
        config_path = get_config_file_path()
        with open(config_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_config(config):
    """Save config to JSON file."""
    config_path = get_config_file_path()
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)


def get_question_text():
    """Get the main question text from config, or return default."""
    config = load_config()
    return config.get("question_text", DEFAULT_QUESTION_TEXT)


def get_evaluation_questions():
    """Get the evaluation questions from config, or return defaults."""
    config = load_config()
    questions = config.get("evaluation_questions", DEFAULT_EVALUATION_QUESTIONS)

    # Ensure we have exactly 2 questions
    if not isinstance(questions, list) or len(questions) != 2:
        return DEFAULT_EVALUATION_QUESTIONS

    return questions


def get_data_dir():
    """Get the data directory for session logs."""
    config = load_config()
    default_dir = os.path.join(os.path.expanduser("~"), ".why_computer")
    data_dir = config.get("data_dir", default_dir)

    # Expand ~ if present
    data_dir = os.path.expanduser(data_dir)
    os.makedirs(data_dir, exist_ok=True)

    return data_dir
