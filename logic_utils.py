"""Core game logic for the Number Guessing Game.

These functions are pure (no Streamlit / no global state) so they can be
unit-tested directly with pytest. app.py imports them for the UI layer.
"""


def get_range_for_difficulty(difficulty: str):
    """Return the inclusive ``(low, high)`` guessing range for a difficulty.

    Unknown difficulties fall back to the Normal range so the game never
    crashes on unexpected input.
    """
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 50),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """Parse raw user input into an integer guess.

    Returns a ``(ok, guess_int, error_message)`` tuple. ``ok`` is False with a
    human-readable ``error_message`` when the input is empty or not a number;
    otherwise ``guess_int`` holds the parsed value. Decimal strings like
    ``"3.7"`` are truncated toward zero (``3``).
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare ``guess`` to ``secret`` and return the outcome string.

    Returns one of ``"Win"``, ``"Too High"``, or ``"Too Low"``. The caller is
    responsible for turning the outcome into a player-facing hint via
    :func:`hint_for_outcome`.
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def hint_for_outcome(outcome: str):
    """Return the player-facing hint message for a given outcome.

    The hints point the player toward the secret: a guess that is "Too High"
    tells them to go LOWER, and "Too Low" tells them to go HIGHER.
    """
    hints = {
        "Win": "🎉 Correct!",
        "Too High": "📉 Too high — go LOWER!",
        "Too Low": "📈 Too low — go HIGHER!",
    }
    return hints.get(outcome, "")


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update the running score after a guess.

    A win awards more points the sooner it happens (``100 - 10 * attempts``,
    floored at 10). Any wrong guess costs a flat 5 points, and the score never
    drops below zero. Scoring is now consistent regardless of attempt parity.
    """
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    return max(0, current_score - 5)
