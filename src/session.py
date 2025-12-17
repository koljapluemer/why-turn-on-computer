"""Session state management for Why Turn On Computer."""
import json
import os
import fcntl
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from .config import get_data_dir


@dataclass
class Session:
    """Represents an active session."""
    reason: str
    start_time: datetime
    timestamp: str

    @staticmethod
    def get_current() -> Optional['Session']:
        """Load current session from file, or return None if no active session."""
        session_file = get_session_file_path()

        if not os.path.exists(session_file):
            return None

        try:
            with lock_session_file():
                with open(session_file, 'r') as f:
                    data = json.load(f)

                return Session(
                    reason=data['reason'],
                    start_time=datetime.fromisoformat(data['start_time']),
                    timestamp=data['timestamp']
                )
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return None

    @staticmethod
    def create(reason: str) -> 'Session':
        """Create and persist a new session."""
        now = datetime.now()
        session = Session(
            reason=reason,
            start_time=now,
            timestamp=now.isoformat()
        )

        session_file = get_session_file_path()

        with lock_session_file():
            with open(session_file, 'w') as f:
                json.dump({
                    'reason': session.reason,
                    'start_time': session.start_time.isoformat(),
                    'timestamp': session.timestamp
                }, f, indent=2)

        return session

    def delete(self) -> None:
        """Remove current session file."""
        session_file = get_session_file_path()

        with lock_session_file():
            if os.path.exists(session_file):
                os.remove(session_file)

    def get_duration(self) -> timedelta:
        """Calculate duration since session start."""
        return datetime.now() - self.start_time

    def format_duration(self) -> str:
        """Return human-readable duration string (e.g., '1h 23m')."""
        duration = self.get_duration()
        total_seconds = int(duration.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"


def get_session_file_path() -> str:
    """Get the path to the current session file."""
    data_dir = get_data_dir()
    return os.path.join(data_dir, ".current_session.json")


def get_lock_file_path() -> str:
    """Get the path to the session lock file."""
    data_dir = get_data_dir()
    return os.path.join(data_dir, ".session.lock")


@contextmanager
def lock_session_file():
    """Context manager for file locking to prevent concurrent access."""
    lock_file = get_lock_file_path()

    # Ensure lock file exists
    Path(lock_file).touch()

    with open(lock_file, 'w') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
