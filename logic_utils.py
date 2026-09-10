import random

# FIX #8: Refactored functions from app.py to logic_utils.py
# User-AI collaboration: User pointed to comments in original logic_utils.py
# requesting refactoring. AI moved all helper functions here for better code organization.

def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX #6: Changed range to 1-100 for all difficulties
    # User-AI collaboration: User requested all difficulties use 1-100 range
    # instead of varying ranges (Easy: 1-20, Normal: 1-100, Hard: 1-50).
    # AI updated function to return consistent 1-100 range.

    # NEW FEATURE: Extra Hard mode with 1-1000 range
    # User-AI collaboration: User requested new "Extra Hard" difficulty with
    # range 1-1000 and only 5 attempts for extreme challenge. AI implemented
    # by adding special case for "Extra Hard" while maintaining 1-100 for others.
    if difficulty == "Extra Hard":
        return 1, 1000
    return 1, 100


def parse_guess(raw: str, low: int = 1, high: int = 100):
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

    # FIX #7: Added range validation to reject numbers outside 1-100
    # User-AI collaboration: User noted that input validation should prevent
    # numbers >100 or <1. AI added this validation check with appropriate error message.
    if value < low or value > high:
        return False, None, f"Number must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX #9: Corrected reversed hint messages
    # User-AI collaboration: AI discovered that "Go HIGHER!" and "Go LOWER!" messages
    # were reversed (when guess > secret, it said "Go HIGHER!" but should say "Go LOWER!").
    # AI fixed the logic to provide correct directional hints.
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # Award points based on how quickly you won
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    # FIX #11: Made scoring logic consistent for wrong guesses
    # User-AI collaboration: AI identified inconsistent scoring where "Too High"
    # on even attempts added 5 points (rewarding wrong guesses). User confirmed
    # this should be fixed. AI simplified logic so all wrong guesses consistently
    # subtract 5 points regardless of guess type or attempt number.
    if outcome == "Too High" or outcome == "Too Low":
        return current_score - 5

    return current_score


def get_random_attempt_limit(difficulty: str):
    """Return a randomized attempt limit based on difficulty."""
    # FIX #2: Randomized attempt limits instead of fixed values
    # User-AI collaboration: User requested that attempts allowed should be
    # randomized rather than fixed. AI created this function to return random
    # attempt limits within appropriate ranges for each difficulty level
    # (Easy: 8-12, Normal: 6-10, Hard: 4-7).

    # NEW FEATURE: Extra Hard mode with fixed 5 attempts
    # User-AI collaboration: User requested "Extra Hard" mode with only 5 attempts
    # (no randomization for this extreme difficulty). AI added fixed 5 attempts
    # for Extra Hard while keeping randomization for other difficulties.
    if difficulty == "Extra Hard":
        return 5
    if difficulty == "Easy":
        return random.randint(8, 12)
    if difficulty == "Normal":
        return random.randint(6, 10)
    if difficulty == "Hard":
        return random.randint(4, 7)
    return random.randint(6, 10)
