DIFFICULTY_SETTINGS = {
    "Easy":   {"range": (1, 20),  "attempts": 10},
    "Normal": {"range": (1, 100), "attempts": 8},
    "Hard":   {"range": (1, 200), "attempts": 5},
}
_DEFAULT = DIFFICULTY_SETTINGS["Normal"]


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    return DIFFICULTY_SETTINGS.get(difficulty, _DEFAULT)["range"]


def get_attempt_limit(difficulty: str) -> int:
    """Return the number of allowed attempts for a given difficulty."""
    return DIFFICULTY_SETTINGS.get(difficulty, _DEFAULT)["attempts"]


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if not raw:
        return False, None, "Enter a guess."

    try:
        value = int(float(raw)) if "." in raw else int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        return current_score + max(10, 100 - 10 * (attempt_number + 1))
    if outcome in ("Too High", "Too Low"):
        return current_score - 5
    return current_score
