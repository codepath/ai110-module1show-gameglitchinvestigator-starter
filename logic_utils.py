def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


# FIX: Refactored check_guess into logic_utils.py using Claude AI Agent mode.
# I (user) identified that the hint messages were swapped and the TypeError fallback
# used str(guess) instead of int(guess), causing wrong lexicographic comparisons.
# Claude helped implement the corrected logic and convert both guess and secret to int
# in the fallback so comparisons are always numeric.
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        # FIX: Messages were originally swapped — "Too High" said "Go HIGHER!" and vice versa.
        # I caught this by reading the hint feedback during gameplay; Claude corrected both branches.
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        # FIX: Original code used str(guess), causing lexicographic comparison bugs
        # (e.g., "9" > "10" is True as strings). I identified the symptom; Claude
        # pinpointed that both guess and secret needed int() conversion here.
        g = int(guess)
        s = int(secret)
        if g == s:
            return "Win", "🎉 Correct!"
        if g > s:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")
