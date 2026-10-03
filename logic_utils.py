
def get_range_for_difficulty(difficulty: str):
    """Return the inclusive secret-number range for a difficulty level.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard". Any other value
            (including unrecognized strings) falls back to the Normal range.

    Returns:
        A ``(low, high)`` tuple of ints giving the inclusive bounds the
        secret number may be drawn from.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Unknown")
        (1, 100)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """Parse raw user input into a validated integer guess.

    Accepts plain integers (e.g. "42") and decimal strings (e.g. "42.9"),
    which are truncated toward zero via ``int(float(raw))``. Empty input or
    ``None`` is treated as a missing guess rather than an invalid one.

    Args:
        raw: The raw text entered by the player, or ``None``.

    Returns:
        A ``(ok, guess_int, error_message)`` tuple:
            - ``ok``: ``True`` if parsing succeeded, else ``False``.
            - ``guess_int``: the parsed integer, or ``None`` if parsing failed.
            - ``error_message``: a user-facing message when ``ok`` is
              ``False``, else ``None``.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("")
        (False, None, 'Enter a guess.')
        >>> parse_guess("banana")
        (False, None, 'That is not a number.')
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

    return True, value, None


def check_guess(guess, secret):
    """Compare a guess to the secret number and classify the outcome.

    Args:
        guess: The player's parsed integer guess.
        secret: The secret number to compare against.

    Returns:
        One of ``"Win"`` (guess equals secret), ``"Too High"`` (guess is
        greater than secret), or ``"Too Low"`` (guess is less than secret).

    Examples:
        >>> check_guess(50, 50)
        'Win'
        >>> check_guess(60, 50)
        'Too High'
        >>> check_guess(40, 50)
        'Too Low'
    """
    # FIX: removed secret-to-str flip and reversed Too High/Too Low messages (Copilot agent mode)
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Apply a scoring adjustment for one guess outcome.

    A win awards ``100 - 10 * attempt_number`` points (never less than a
    10-point floor), rewarding earlier correct guesses more. Any wrong guess
    ("Too High" or "Too Low") always deducts 5 points, with no lower bound.
    Unrecognized outcomes leave the score unchanged.

    Args:
        current_score: The player's score before this guess.
        outcome: The result of the guess, as returned by ``check_guess``
            (``"Win"``, ``"Too High"``, or ``"Too Low"``).
        attempt_number: The 1-based attempt count this guess was made on,
            used only for the win-score formula.

    Returns:
        The updated score as an int.

    Examples:
        >>> update_score(0, "Win", attempt_number=1)
        90
        >>> update_score(0, "Too High", attempt_number=2)
        -5
    """
    if outcome == "Win":
        # FIX: dropped the extra +1 that under-scored every win by 10 points (Copilot agent mode)
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        # FIX: removed even-attempt bonus that rewarded a wrong guess (Copilot agent mode)
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


def get_proximity_label(guess: int, secret: int, low: int, high: int) -> str:
    """Return a Hot/Warm/Cold label describing how close a guess was.

    Distance is measured relative to the size of the difficulty's range, so
    the same numeric distance reads "hotter" on a small range (e.g. Easy)
    than on a large one (e.g. Normal).

    Args:
        guess: The player's guess.
        secret: The secret number.
        low: The inclusive lower bound of the difficulty's range.
        high: The inclusive upper bound of the difficulty's range.

    Returns:
        ``"🎯 Spot On!"`` for an exact match, ``"🔥 Hot"`` when within 15% of
        the range size, ``"🌡️ Warm"`` within 50%, otherwise ``"🧊 Cold"``.

    Examples:
        >>> get_proximity_label(50, 50, 1, 100)
        '🎯 Spot On!'
        >>> get_proximity_label(48, 50, 1, 100)
        '🔥 Hot'
        >>> get_proximity_label(100, 50, 1, 100)
        '🧊 Cold'
    """
    if guess == secret:
        return "🎯 Spot On!"

    range_size = max(high - low, 1)
    distance = abs(guess - secret)
    closeness = max(0.0, 1 - (distance / range_size))

    if closeness >= 0.85:
        return "🔥 Hot"
    if closeness >= 0.5:
        return "🌡️ Warm"
    return "🧊 Cold"
