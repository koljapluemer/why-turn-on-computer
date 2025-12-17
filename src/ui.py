"""UI components using prompt_toolkit."""
from typing import Optional, List, Tuple
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import radiolist_dialog

from .session import Session


def prompt_for_reason(question_text: str) -> str:
    """Prompt for session reason."""
    print()
    print(question_text)
    result = prompt('> ')
    return result.strip()


def display_current_session(session: Session) -> None:
    """Display current session with duration."""
    print()
    print(f'Current session started at {session.start_time.strftime("%H:%M")}')
    print()
    print(f'  "{session.reason}"')
    print()
    print(f'Session duration: {session.format_duration()}')
    print()


def prompt_evaluation_form(questions: List[str], session: Session) -> Optional[Tuple[List[int], str]]:
    """Evaluation form with Likert scales and comment.

    Returns (answers, comment) or None if cancelled.
    """
    print()
    print(f'Session: "{session.reason}"')
    print(f'Duration: {session.format_duration()}')
    print()

    answers = []

    # Ask each question
    for i, question in enumerate(questions, 1):
        answer = radiolist_dialog(
            title=f'Question {i}/{len(questions)}',
            text=question,
            values=[
                (1, '1 - Not at all'),
                (2, '2'),
                (3, '3 - Somewhat'),
                (4, '4'),
                (5, '5 - Very much'),
            ]
        ).run()

        if answer is None:
            return None

        answers.append(answer)

    # Ask for comment
    print()
    print('Any additional comments? (Press Esc+Enter when done, or just Enter to skip)')
    try:
        comment = prompt('> ', multiline=True)
    except (KeyboardInterrupt, EOFError):
        return None

    return (answers, comment.strip())


def display_success(message: str) -> None:
    """Show success message."""
    print()
    print(message)
    print()


def display_error(message: str) -> None:
    """Show error message."""
    print()
    print(f'Error: {message}')
    print()
