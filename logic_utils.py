def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Copilot handled difficulty change flawlessly as it was a simple bug.
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 50),
        "Hard": (1, 100),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: Moved logic into logic_utils.py using Copilot Agent mode
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: Told Copilot Agent fix only this function in app.py and port it to logic_utils.py
    guess_value = int(guess)
    secret_value = int(secret)

    if guess_value == secret_value:
        return "Win", "🎉 Correct!"

    if guess_value > secret_value:
        return "Too High", "📉 Go LOWER!"

    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX: Moved logic into logic_utils.py using Copilot Agent mode
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
