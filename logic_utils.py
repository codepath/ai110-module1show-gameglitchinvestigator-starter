"""Pure game logic for the number-guessing game.

Nothing in here imports Streamlit or touches session state, which is what
makes it straightforward to unit test with pytest.
"""

# Difficulty -> (low, high) inclusive guessing range.
DIFFICULTY_RANGES = {
    "Easy": (1, 20),
    "Normal": (1, 100),
    "Hard": (1, 50),
}

# Difficulty -> how many valid guesses the player gets.
# Each limit is at least ceil(log2(range size)) so a player using binary
# search can always win. "Hard" has the least slack.
ATTEMPT_LIMITS = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 6,
}

DEFAULT_DIFFICULTY = "Normal"

# The hint tells the player which way to move NEXT, so it is the opposite of
# the outcome: a guess that was too high means they must go lower.
OUTCOME_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}

WIN_BASE_POINTS = 100
WIN_POINTS_PER_ATTEMPT = 10
MIN_WIN_POINTS = 10
WRONG_GUESS_PENALTY = 5


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    return DIFFICULTY_RANGES.get(difficulty, DIFFICULTY_RANGES[DEFAULT_DIFFICULTY])


def get_attempt_limit(difficulty: str) -> int:
    """Return how many valid guesses the player gets for a difficulty."""
    return ATTEMPT_LIMITS.get(difficulty, ATTEMPT_LIMITS[DEFAULT_DIFFICULTY])


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    raw = raw.strip()
    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome as a string.

    Returns one of: "Win", "Too High", "Too Low"

    Both values are coerced to int so the comparison is always numeric.
    Comparing a number against a string would either raise TypeError or, if
    both were strings, compare them alphabetically ("9" > "10").
    """
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def get_hint_message(outcome: str) -> str:
    """Return the player-facing hint for an outcome from check_guess()."""
    return OUTCOME_MESSAGES.get(outcome, "")


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    `attempt_number` is the 1-based number of the guess just made, so winning
    on the very first guess is worth the full WIN_BASE_POINTS. Every wrong
    guess costs the same, regardless of direction.
    """
    if outcome == "Win":
        points = WIN_BASE_POINTS - WIN_POINTS_PER_ATTEMPT * (attempt_number - 1)
        return current_score + max(points, MIN_WIN_POINTS)

    if outcome in ("Too High", "Too Low"):
        return current_score - WRONG_GUESS_PENALTY

    return current_score
