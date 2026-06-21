"""Game logic utilities: range selection, input parsing, guess checking, and scoring."""


def get_range_for_difficulty(difficulty: str):
    """Return the inclusive numeric range for a given difficulty level.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard". Any unrecognized
            value falls back to the Normal range.

    Returns:
        A tuple (low, high) of ints representing the inclusive bounds
        within which the secret number will be generated.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 50)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str, low: int, high: int):
    """Parse and validate raw user input as an integer guess within [low, high].

    Accepts whole numbers and decimal strings (e.g. "7.0"), truncating any
    fractional part. Returns a structured result tuple so the caller can
    handle errors without catching exceptions.

    Args:
        raw: The raw string typed by the user. May be None, empty, non-numeric,
            or out of range.
        low: The inclusive lower bound of the valid guess range.
        high: The inclusive upper bound of the valid guess range.

    Returns:
        A three-tuple (ok, guess_int, error_message):
            - ok (bool): True if the input was valid, False otherwise.
            - guess_int (int | None): The parsed integer on success, None on failure.
            - error_message (str | None): A human-readable error string on failure,
              None on success.

    Examples:
        >>> parse_guess("42", 1, 100)
        (True, 42, None)
        >>> parse_guess("abc", 1, 100)
        (False, None, 'That is not a number.')
        >>> parse_guess("200", 1, 100)
        (False, None, 'Guess must be between 1 and 100.')
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    # Parse first, THEN range-check. Doing the bounds check before this
    # try/except would crash on non-numeric input like "abc".
    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Guess must be between {low} and {high}."
    return True, value, None


def check_guess(guess, secret):
    """Compare a player's guess against the secret number and return a result.

    Both arguments are coerced to int before comparison, preventing subtle
    bugs from str/int type mismatches (e.g. lexicographic ordering where
    "9" > "10" would produce wrong hints).

    Args:
        guess: The player's guessed value. Accepts int or a numeric string.
        secret: The target number to guess. Accepts int or a numeric string.

    Returns:
        A two-tuple (outcome, message):
            - outcome (str): One of "Win", "Too High", or "Too Low".
            - message (str): A short, emoji-prefixed hint suitable for display.

    Examples:
        >>> check_guess(42, 42)
        ('Win', '🎉 Correct!')
        >>> check_guess(80, 42)
        ('Too High', '📉 Go LOWER!')
        >>> check_guess(10, 42)
        ('Too Low', '📈 Go HIGHER!')
    """
    # Normalize both values to int so comparisons are always numeric.
    # Previously a str/int type mismatch fell back to lexicographic string
    # comparison (e.g. "9" > "10" is True), producing wrong high/low hints.
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Compute the new cumulative score after a single guess attempt.

    Scoring rules:
        - Win: awards ``max(10, 100 - 10 * (attempt_number - 1))`` points,
          rewarding faster wins with higher scores and flooring at 10.
        - Too High / Too Low: deducts 5 points, floored at 0 so the score
          never goes negative.
        - Any other outcome: score is unchanged.

    Args:
        current_score: The player's score before this attempt.
        outcome: The result string from ``check_guess`` — one of "Win",
            "Too High", or "Too Low".
        attempt_number: The 1-based index of the current attempt (1 = first guess).

    Returns:
        The updated integer score after applying the outcome.

    Examples:
        >>> update_score(0, "Win", 1)
        100
        >>> update_score(0, "Win", 5)
        60
        >>> update_score(20, "Too High", 3)
        15
        >>> update_score(0, "Too Low", 1)
        0
    """
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number - 1))
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return max(0, current_score - 5)

    return current_score
