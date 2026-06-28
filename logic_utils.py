def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # Make difficulty monotonic: Easy < Normal < Hard
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str, low: int, high: int):
    """
    Parse user input into an int guess and validate the current difficulty range.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        # Accept floats only if they are whole numbers (e.g. '7.0').
        # Reject non-integer floats (e.g. '9.9') to avoid silent truncation.
        f = float(raw)
        if not f.is_integer():
            return False, None, "Please enter a whole number."
        value = int(f)
    except ValueError:
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Guess must be between {low} and {high}."

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


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # attempt_number is 1-indexed in the app (first attempt == 1)
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    # For any non-winning guess, apply a symmetric penalty.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
