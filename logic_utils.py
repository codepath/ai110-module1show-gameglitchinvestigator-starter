from __future__ import annotations

from typing import Tuple


def get_range_for_difficulty(difficulty: str) -> Tuple[int, int]:
    """
    Return the inclusive (low, high) range for the given difficulty.

    The UI uses this range to generate a secret number and validate guesses.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str | None) -> tuple[bool, int | None, str | None]:
    """
    Parse user input into an integer guess.

    Returns:
        ok: Whether parsing succeeded.
        guess_int: Parsed integer guess when ok is True, otherwise None.
        error_message: Human-friendly error when ok is False, otherwise None.

    Notes:
        - Decimal strings are accepted and truncated toward zero (e.g., "3.9" -> 3).
        - Range validation is handled by the Streamlit UI (not here).
    """
    if raw is None:
        return False, None, "Enter a guess."

    text = str(raw).strip()
    if text == "":
        return False, None, "Enter a guess."

    try:
        if "." in text:
            value = int(float(text))
        else:
            value = int(text)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> str:
    """
    Compare guess to secret and return the outcome label.

    Returns:
        "Win" if guess == secret,
        "Too High" if guess > secret,
        "Too Low" otherwise.
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """
    Update the player's score.

    The scoring rule is intentionally simple:
        - Win: add points based on how quickly you won (minimum 10 points).
        - Otherwise: small penalty.
    """
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        return current_score + max(points, 10)

    return current_score - 5
