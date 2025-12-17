#!/usr/bin/env python3
"""
End current session with evaluation.

Usage: why-done
"""
import sys
from datetime import datetime
from src.session import Session, lock_session_file
from src.storage import CompletedSession
from src.ui import (
    display_error,
    prompt_evaluation_form,
    display_success
)
from src.config import get_evaluation_questions


def main():
    try:
        with lock_session_file():
            # Check for active session
            session = Session.get_current()

            if not session:
                display_error("No active session to end.")
                print("Start a session first with the 'why' command.")
                sys.exit(1)

            # Show full-screen evaluation form
            questions = get_evaluation_questions()
            result = prompt_evaluation_form(questions, session)

            if result is None:
                print("\nCancelled.")
                sys.exit(0)

            answers, comment = result

            # Build evaluations dict
            evaluations = {q: a for q, a in zip(questions, answers)}

            # Save completed session
            completed = CompletedSession(
                reason=session.reason,
                start_time=session.start_time,
                end_time=datetime.now(),
                duration=session.get_duration().total_seconds(),
                evaluations=evaluations,
                comment=comment
            )

            log_path = completed.save()

            # Clean up current session
            session.delete()

            # Success message
            display_success("Session completed and saved!")
            print(f"Log: {log_path}\n")

    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)
    except Exception as e:
        display_error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
