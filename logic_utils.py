def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
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
    """
    Compare guess to secret and return the outcome string.

    Returns one of: "Win", "Too High", "Too Low"
    # FIX: Original code had inverted hints — "Go HIGHER!" when guess > secret
    # and "Go LOWER!" when guess < secret. Fixed by swapping the messages.
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    # FIX: Original code added/subtracted points on every wrong guess,
    # causing erratic score changes. Now only Win changes the score.
    """
    if outcome == "Win":
        points = max(10, 100 - 10 * attempt_number)
        return current_score + points
    return current_score
