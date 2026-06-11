"""Core game logic utilities for the Number Guessing Game.

Refactored from app.py stubs into this module so tests/test_game_logic.py
can import and exercise them independently.
"""


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive (low, high) number range for a difficulty level.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard". Any other value
            falls back to the Normal range.

    Returns:
        A tuple (low, high) representing the inclusive guess range.
        Easy → (1, 20), Normal → (1, 100), Hard → (1, 50).
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """Parse raw user input into a validated integer guess.

    Accepts whole numbers and decimal strings (e.g. "7.0" → 7).
    Rejects empty/None input and non-numeric strings.

    Args:
        raw: The raw string entered by the user, possibly None or empty.

    Returns:
        A 3-tuple (ok, guess_int, error_message):
            - ok: True when parsing succeeded, False otherwise.
            - guess_int: The parsed integer on success, None on failure.
            - error_message: A human-readable error string on failure,
              None on success.
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> str:
    """Compare a guess to the secret number and return the outcome.

    Args:
        guess: The player's guessed integer.
        secret: The target secret integer.

    Returns:
        "Win" if guess equals secret, "Too High" if guess exceeds secret,
        or "Too Low" if guess is below secret.
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Update and return the score based on the outcome of a guess.

    Winning awards 100 points minus 10 per attempt (1-indexed), with a
    minimum of 10 points. Each wrong guess deducts 5 points. Unknown
    outcomes leave the score unchanged.

    Args:
        current_score: The player's score before this guess.
        outcome: The result string — "Win", "Too High", or "Too Low".
        attempt_number: Zero-based index of the current attempt.

    Returns:
        The updated integer score after applying the outcome.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score


def guess_distance(guess: int, secret: int) -> int:
    """Return the absolute difference between guess and secret.

    Both arguments are cast to int before subtraction. Returns a large
    sentinel value (10_000) when either argument cannot be converted.

    Args:
        guess: The player's guess value (int or int-castable).
        secret: The secret number (int or int-castable).

    Returns:
        Non-negative integer distance, or 10_000 on conversion error.
    """
    try:
        return abs(int(guess) - int(secret))
    except (ValueError, TypeError):
        return 10_000


def closeness(distance: int, span: int) -> tuple[float, str]:
    """Compute a closeness fraction and label given a distance and range span.

    The fraction is clamped to [0.0, 1.0]. Labels are assigned by threshold:
    fraction >= 0.85 → "🔥 Hot", >= 0.5 → "🌤️ Warm", else → "❄️ Cold".
    A span of zero or less is treated as 1 to avoid division by zero.

    Args:
        distance: Absolute distance between guess and secret.
        span: Total size of the number range (high − low).

    Returns:
        A 2-tuple (fraction, label) where fraction is a float in [0.0, 1.0]
        and label is one of "🔥 Hot", "🌤️ Warm", or "❄️ Cold".
    """
    if span <= 0:
        span = 1
    fraction = max(0.0, 1.0 - distance / span)
    if fraction >= 0.85:
        label = "🔥 Hot"
    elif fraction >= 0.5:
        label = "🌤️ Warm"
    else:
        label = "❄️ Cold"
    return fraction, label


def label_color(label: str) -> str:
    """Map a closeness label to a Streamlit markdown color token.

    Returns "red", "orange", or "blue" for Hot/Warm/Cold respectively;
    "gray" for unknown or empty labels (e.g. Invalid guesses).
    Pure/stateless — no Streamlit dependency.

    Args:
        label: A closeness label string such as "🔥 Hot", "🌤️ Warm",
            or "❄️ Cold". Matching is substring-based.

    Returns:
        A lowercase color token suitable for use in Streamlit's
        :color[text] markdown syntax.
    """
    if "Hot" in label:
        return "red"
    if "Warm" in label:
        return "orange"
    if "Cold" in label:
        return "blue"
    return "gray"


def history_to_rows(history: list) -> list:
    """Convert session history records into display rows for st.dataframe.

    Each record in history is a dict with keys: attempt, guess, outcome,
    fraction (float or None), label (str). Invalid guesses (fraction is
    None) render Temperature and Closeness % as "—".

    Args:
        history: List of guess-record dicts from st.session_state.history.

    Returns:
        List of flat dicts with keys "Attempt #", "Guess", "Outcome",
        "Temperature", "Closeness %" ready for st.dataframe.
    """
    rows = []
    for rec in history:
        frac = rec.get("fraction")
        rows.append({
            "Attempt #": rec.get("attempt"),
            "Guess": rec.get("guess"),
            "Outcome": rec.get("outcome", ""),
            "Temperature": rec.get("label") or "—",
            "Closeness %": f"{round(frac * 100)}%" if frac is not None else "—",
        })
    return rows
