"""Pure game logic for the Glitchy Guesser.

Deliberately contains no Streamlit imports, so every function here can be
unit tested with pytest without spinning up a browser session.

# FIX: Refactored out of app.py with AI assistance. The starter mixed game
# rules into the UI file, which made the rules untestable -- the bugs below
# were invisible until the logic could be called directly from pytest.
"""

# Difficulty -> (low, high) inclusive guessing range.
# FIX: "Hard" was 1-50 in the starter, which is a NARROWER range than
# "Normal" (1-100) and therefore easier. Widened so difficulty is monotonic.
_RANGES = {
    "Easy": (1, 20),
    "Normal": (1, 100),
    "Hard": (1, 200),
}

# Difficulty -> number of attempts allowed.
# Roughly log2(range size), so every difficulty is winnable by halving.
_ATTEMPT_LIMITS = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 10,
}


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    return _RANGES.get(difficulty, _RANGES["Normal"])


def get_attempt_limit(difficulty: str):
    """Return how many guesses the player gets on a given difficulty."""
    return _ATTEMPT_LIMITS.get(difficulty, _ATTEMPT_LIMITS["Normal"])


def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)

    # FIX: the starter accepted any integer, so "999" was a legal guess on
    # Easy (range 1-20). It also silently truncated "50.9" to 50 via
    # int(float(raw)), telling the player nothing. Both now rejected.
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        value = int(raw.strip())
    except ValueError:
        return False, None, "That is not a whole number."

    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome as a single string.

    Returns one of: "Win", "Too High", "Too Low"

    # FIX: two bugs killed here.
    #   1. The starter returned a (outcome, message) tuple, and the message
    #      contradicted the outcome -- "Too High" was paired with
    #      "Go HIGHER!". Messages now live in hint_message() so the outcome
    #      and the advice cannot drift apart again.
    #   2. The starter had a bare `except TypeError` that fell back to
    #      comparing the values as TEXT. Text comparison is alphabetical, so
    #      "9" > "100" is True. Coercing both sides to int up front means a
    #      bad type now raises loudly instead of silently lying.
    """
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def hint_message(outcome: str):
    """
    Return the player-facing hint for an outcome.

    # FIX: single source of truth for hint direction. "Too High" means the
    # guess was ABOVE the secret, so the player must come DOWN.
    """
    if outcome == "Win":
        return "🎉 Correct!"
    if outcome == "Too High":
        return "📉 Too high - go LOWER!"
    return "📈 Too low - go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    attempt_number is 1-based, so winning on the first guess scores highest.

    # FIX: the starter awarded +5 for a "Too High" guess on even attempts and
    # -5 on odd ones, so an identical wrong guess helped or hurt depending on
    # turn parity. Every wrong guess now costs the same regardless of
    # direction or turn. Score is also floored at 0 so it cannot go negative.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        return current_score + max(points, 10)

    return max(current_score - 5, 0)
