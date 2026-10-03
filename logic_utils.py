import random

# FIX: I asked AI to help isolate the comparison logic, then checked the result against the hint rules. I kept the change so the app uses consistent secret types.
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # UPDATE: I asked AI to change Easy to 1-50 and Hard to 1-150. I checked the mapping and tested both ranges against what I wanted in the game.
    ranges = {
        "Easy": (1, 50),
        "Normal": (1, 100),
        "Hard": (1, 150),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: I asked AI to help handle empty and invalid input. I checked the suggested parsing and kept the clear error instead of letting bad input break the game flow.
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        value = int(float(raw)) if "." in raw else int(raw)
    except (TypeError, ValueError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: I worked with AI to track down why the hints were wrong when a string was compared with an int. I checked the fix and normalized the comparison to numeric values.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX: I asked AI to help trace why the score changed after the game should have ended. I reviewed the refactor and kept the centralized update so a win adds the bonus once, a score below zero ends the game, and non-win guesses change the score once per submit.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    list1 = [4, -10]
    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + random.choice(list1)
        return current_score - 5

    if outcome == "Too Low":
        if attempt_number % 2 != 0:
            return current_score + random.choice(list1)
        return current_score - 5

    return current_score
