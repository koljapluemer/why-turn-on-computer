"""Data persistence for completed sessions."""
import os
from datetime import datetime
from dataclasses import dataclass
from typing import Dict

from .config import get_data_dir


@dataclass
class CompletedSession:
    """Represents a completed session ready to be saved."""
    reason: str
    start_time: datetime
    end_time: datetime
    duration: float
    evaluations: Dict[str, int]  # question -> answer (1-5)
    comment: str

    def save(self) -> str:
        """Save session to log file. Returns the path to the saved file."""
        data_dir = get_data_dir()
        log_file_path = os.path.join(
            data_dir,
            f'session_{self.start_time.isoformat()}.txt'
        )

        content = self._format_log()

        with open(log_file_path, 'w') as f:
            f.write(content)

        return log_file_path

    def _format_log(self) -> str:
        """Format session data as key=value lines."""
        lines = [
            f"start_time={self.start_time.isoformat()}",
            f"reason={self.reason}",
            f"duration={self.duration}",
        ]

        # Add evaluation questions and answers
        for i, (question, answer) in enumerate(self.evaluations.items(), 1):
            lines.append(f"question_{i}={question}")
            lines.append(f"answer_{i}={answer}")

        # Add comment and end time
        lines.append(f"comment={self.comment}")
        lines.append(f"end_time={self.end_time.isoformat()}")

        return "\n".join(lines) + "\n"
