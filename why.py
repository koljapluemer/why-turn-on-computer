#!/usr/bin/env python3
"""
Display current session reason or start new session.

Usage: why
"""
import sys
from src.session import Session
from src.ui import (
    display_current_session,
    prompt_for_reason,
    display_success,
    display_error
)
from src.config import get_question_text


def main():
    try:
        # Check for active session
        session = Session.get_current()

        if session:
            # Display existing session
            display_current_session(session)
        else:
            # No active session - prompt to start one
            print("No active session.")
            question = get_question_text()
            reason = prompt_for_reason(question)

            if reason:
                session = Session.create(reason)
                display_success(f"Session started: {reason}")
            else:
                print("Cancelled.")
                sys.exit(0)

    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)
    except Exception as e:
        display_error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
