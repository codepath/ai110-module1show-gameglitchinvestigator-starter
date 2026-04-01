def get_range_for_difficulty(difficulty: str):      #FIX: Refactored logic into logic_utils.py using Copilot Agent mode, and changed Normal and Hard ranges.
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100     


def parse_guess(raw: str):        #FIX: Refactored logic into logic_utils.py using Copilot Agent mode. Now does not accept zero or negative numbers.
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
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

    if value <= 0:
        return False, None, "Guess must be a positive number greater than zero."

    return True, value, None


def check_guess(guess, secret):     #FIX: Refactored logic into logic_utils.py using Copilot Agent mode
    """Check the user's guess against the secret and return outcome and message."""
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):     #FIX: Refactored logic into logic_utils.py using Copilot Agent mode, and changed scoring to be more balanced.
    """Update score based on outcome and attempt number.

    The score is never allowed to go below 0.
    """
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return max(current_score - 5, 0)

    return max(current_score, 0)
