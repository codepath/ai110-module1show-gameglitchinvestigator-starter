"""Pure game logic for the number-guessing game.

Everything in here is deliberately free of Streamlit imports so it can be
imported and unit tested without booting a web server. `app.py` owns the UI and
session state; this module owns the rules.

# FIX: All four functions were refactored out of app.py with Claude Code in
# agent mode. I asked it to move the functions, fix the inverted hints and the
# string-comparison bug, and update the imports in app.py in one pass, then
# reviewed the diff function by function before keeping it.
"""

import math

# Outcome constants. app.py used bare string literals in five different places,
# which is how "Too High" ended up paired with "go HIGHER" -- a typo in any one
# of them failed silently. Naming them means a typo is an AttributeError.
WIN = "Win"
TOO_HIGH = "Too High"
TOO_LOW = "Too Low"

# Scoring knobs, named so the numbers are not magic.
MAX_WIN_POINTS = 100
MIN_WIN_POINTS = 10
POINTS_LOST_PER_ATTEMPT = 10
WRONG_GUESS_PENALTY = 5

# (low, high, attempts) per difficulty.
#
# # FIX: "Hard" used to be 1-50, a NARROWER range than "Normal" (1-100), so
# Hard was the easiest setting in the game. Hard is now the widest range.
#
# The attempt budget for each row must be at least ceil(log2(number of
# possibilities)), otherwise the difficulty is unwinnable even with perfect
# binary-search play. Easy needs 5 and gets 6, Normal needs 7 and gets 8, Hard
# needs 8 and gets 8. `test_every_difficulty_is_winnable_by_binary_search`
# enforces that so a future tweak to this table cannot quietly ship an
# impossible difficulty.
DIFFICULTIES = {
    "Easy": (1, 20, 6),
    "Normal": (1, 100, 8),
    "Hard": (1, 200, 8),
}

DEFAULT_DIFFICULTY = "Normal"


def get_range_for_difficulty(difficulty: str):
    """Return the inclusive guessing range for a difficulty.

    Args:
        difficulty: A key of :data:`DIFFICULTIES`, e.g. ``"Easy"``. Unknown
            values fall back to Normal rather than raising, because this value
            arrives from a UI widget and a crash there would take the page down.

    Returns:
        A ``(low, high)`` tuple of inclusive bounds.
    """
    low, high, _attempts = DIFFICULTIES.get(
        difficulty, DIFFICULTIES[DEFAULT_DIFFICULTY]
    )
    return low, high


def get_attempt_limit(difficulty: str) -> int:
    """Return how many guesses a difficulty allows.

    Args:
        difficulty: A key of :data:`DIFFICULTIES`. Unknown values fall back to
            Normal, matching :func:`get_range_for_difficulty`.

    Returns:
        The number of attempts allowed at that difficulty.

    # FIX: this lived as a bare `attempt_limit_map` dict inside app.py, one
    # screen away from get_range_for_difficulty, so the range and the attempt
    # budget could drift apart unnoticed. They are one table now.
    """
    _low, _high, attempts = DIFFICULTIES.get(
        difficulty, DIFFICULTIES[DEFAULT_DIFFICULTY]
    )
    return attempts


def minimum_attempts_needed(low: int, high: int) -> int:
    """Return the guesses a perfect binary search needs over a range.

    Args:
        low: Inclusive lower bound.
        high: Inclusive upper bound.

    Returns:
        ``ceil(log2(n))`` for a range of ``n`` possibilities, and 1 for a range
        with a single value (where the log would be 0).
    """
    possibilities = high - low + 1
    if possibilities <= 1:
        return 1
    return math.ceil(math.log2(possibilities))


def parse_guess(raw, low=None, high=None):
    """Parse raw text input into an integer guess.

    Args:
        raw: The text the player typed. ``None`` and blank input are handled.
        low: Optional inclusive lower bound to range-check against.
        high: Optional inclusive upper bound to range-check against.

    Returns:
        A ``(ok, guess_int, error_message)`` tuple. On success that is
        ``(True, <int>, None)``; on failure ``(False, None, "<why>")``, where
        the message is written for the player rather than the developer.

    # FIX: the original accepted "3.9" and silently truncated it to 3 via
    # int(float(raw)), so the game scored you against a number you never
    # guessed. Whole-number decimals like "42.0" are still accepted, but a
    # fractional guess is now an explicit error instead of a silent rewrite.
    #
    # The .strip() is here because the original only tested `raw == ""`, so
    # whitespace-only input fell through to int("   ") and reported "That is
    # not a number." instead of "Enter a guess.". (I first assumed it was
    # needed because " 42" failed to parse -- it did not. Python's int()
    # already strips surrounding whitespace. See reflection.md section 2.)
    """
    if raw is None:
        return False, None, "Enter a guess."

    text = str(raw).strip()
    if text == "":
        return False, None, "Enter a guess."

    try:
        if "." in text or "e" in text.lower():
            as_float = float(text)
            # Guard against inf/nan: float("1e999") is inf, and int(inf) raises
            # OverflowError, which would crash the app rather than show an
            # error. Found while writing test_absurdly_large_input_is_rejected.
            if math.isinf(as_float) or math.isnan(as_float):
                return False, None, "That is not a number."
            if as_float != int(as_float):
                return False, None, "Whole numbers only -- no decimals."
            value = int(as_float)
        else:
            value = int(text)
    except ValueError:
        return False, None, "That is not a number."

    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Out of range. Guess between {low} and {high}."

    return True, value, None


def _to_int(value, name):
    """Coerce a guess/secret to int, refusing anything not numeric.

    # FIX: the original check_guess wrapped its comparison in a bare
    # `except TypeError` that fell back to comparing str(guess) against the
    # secret. That turned a real type error into a LEXICOGRAPHIC comparison --
    # "9" > "50" is True -- which is exactly why the hints lied. Bad types now
    # raise loudly instead of producing a confident wrong answer.
    """
    if isinstance(value, bool):
        raise TypeError(f"{name} must be a number, got bool: {value!r}")
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if value != int(value):
            raise TypeError(f"{name} must be a whole number, got {value!r}")
        return int(value)
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            raise TypeError(f"{name} must be a number, got {value!r}") from None
    raise TypeError(f"{name} must be a number, got {type(value).__name__}: {value!r}")


def check_guess(guess, secret):
    """Compare a guess to the secret and return the outcome.

    Args:
        guess: The player's guess. Numeric strings are accepted and coerced.
        secret: The number being guessed, same rules.

    Returns:
        One of the :data:`WIN`, :data:`TOO_HIGH` or :data:`TOO_LOW` constants.
        Use :func:`hint_message` to turn an outcome into player-facing text.

    Raises:
        TypeError: If either argument is not numeric. Failing loudly is
            deliberate -- see :func:`_to_int`.

    # FIX: this used to return an (outcome, message) tuple, which mixed the
    # rule with its presentation and let them disagree -- TOO_HIGH shipped
    # paired with "Go HIGHER!". Splitting them means the hint text is derived
    # from the outcome instead of hand-written next to it, so they cannot drift
    # apart again. It also matches what the starter tests already asserted.
    """
    guess_int = _to_int(guess, "guess")
    secret_int = _to_int(secret, "secret")

    if guess_int == secret_int:
        return WIN
    if guess_int > secret_int:
        return TOO_HIGH
    return TOO_LOW


def hint_message(outcome: str) -> str:
    """Return the player-facing hint for an outcome.

    Args:
        outcome: One of the :data:`WIN`, :data:`TOO_HIGH` or :data:`TOO_LOW`
            constants.

    Returns:
        A short emoji-prefixed message, or ``""`` for an unrecognised outcome.

    # FIX: the advice is now looked up from the outcome, so "Too High" can only
    # ever tell the player to go LOWER. This is the actual inverted-hint fix.
    """
    return {
        WIN: "🎉 Correct!",
        TOO_HIGH: "📉 Too high -- go LOWER!",
        TOO_LOW: "📈 Too low -- go HIGHER!",
    }.get(outcome, "")


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Return the new score after one guess.

    Args:
        current_score: The score before this guess.
        outcome: One of the :data:`WIN`, :data:`TOO_HIGH` or :data:`TOO_LOW`
            constants. Anything else leaves the score untouched.
        attempt_number: The 1-based number of the attempt just played, so a win
            on the very first guess is worth the full :data:`MAX_WIN_POINTS`.

    Returns:
        The updated score, never below zero.

    # FIX: three bugs here.
    # 1. "Too High" paid +5 on even attempts and -5 on odd ones, so the reward
    #    depended on WHEN you guessed rather than WHAT you guessed. Both wrong
    #    outcomes now cost the same fixed penalty.
    # 2. Nothing clamped the total, so four honest wrong guesses left the score
    #    at -20. The floor is 0.
    # 3. The win bonus was 100 - 10 * (attempt_number + 1), but app.py had
    #    already incremented attempts before calling, so a first-guess win paid
    #    80 instead of 100 -- an off-by-two.
    """
    if outcome == WIN:
        attempts_used = max(1, attempt_number)
        points = MAX_WIN_POINTS - POINTS_LOST_PER_ATTEMPT * (attempts_used - 1)
        points = max(MIN_WIN_POINTS, points)
        return current_score + points

    if outcome in (TOO_HIGH, TOO_LOW):
        return max(0, current_score - WRONG_GUESS_PENALTY)

    # Unknown outcome (e.g. invalid input that never reached check_guess):
    # leave the score alone rather than guessing.
    return current_score


# ---------------------------------------------------------------------------
# Hot/Cold proximity feedback  (stretch feature: Enhanced Game UI)
# ---------------------------------------------------------------------------

# Bands are expressed as a fraction of the difficulty's full range, not as
# absolute distances, so "Hot" means the same thing on Easy (1-20) as it does
# on Hard (1-200). Ordered nearest-first; the first band whose threshold the
# guess falls within wins.
PROXIMITY_BANDS = (
    (0.00, "🎯 Bullseye"),
    (0.05, "🔥 Blazing hot"),
    (0.15, "♨️ Hot"),
    (0.30, "🌤️ Warm"),
    (0.50, "🧊 Cold"),
)
FREEZING_LABEL = "❄️ Freezing"


def proximity_label(guess, secret, low: int, high: int) -> str:
    """Return a Hot/Cold label describing how near a guess is to the secret.

    The distance is normalised against the width of the playing range, so the
    labels mean the same thing at every difficulty: a guess 10 away is "Hot" on
    Hard (1-200) but "Cold" on Easy (1-20), which is the intuition a player
    actually has.

    Args:
        guess: The player's guess.
        secret: The number being guessed.
        low: Inclusive lower bound of the current difficulty's range.
        high: Inclusive upper bound of the current difficulty's range.

    Returns:
        A short emoji-prefixed label, e.g. ``"♨️ Hot"``.
    """
    guess_int = _to_int(guess, "guess")
    secret_int = _to_int(secret, "secret")

    span = max(1, high - low)
    distance_fraction = abs(guess_int - secret_int) / span

    for threshold, label in PROXIMITY_BANDS:
        if distance_fraction <= threshold:
            return label
    return FREEZING_LABEL


def proximity_trend(previous_guess, guess, secret) -> str:
    """Say whether this guess moved nearer to or further from the secret.

    Args:
        previous_guess: The guess before this one, or ``None`` on the first
            guess of a round.
        guess: The guess just played.
        secret: The number being guessed.

    Returns:
        ``"warmer"``, ``"colder"``, ``"same"``, or ``""`` when there is no
        previous guess to compare against.
    """
    if previous_guess is None:
        return ""

    secret_int = _to_int(secret, "secret")
    before = abs(_to_int(previous_guess, "previous_guess") - secret_int)
    after = abs(_to_int(guess, "guess") - secret_int)

    if after < before:
        return "warmer"
    if after > before:
        return "colder"
    return "same"


def build_session_table(history, secret, low: int, high: int):
    """Build a row-per-guess summary of a round, for display as a table.

    Args:
        history: The guesses played this round, oldest first.
        secret: The number being guessed.
        low: Inclusive lower bound of the current difficulty's range.
        high: Inclusive upper bound of the current difficulty's range.

    Returns:
        A list of dicts with the keys ``#``, ``Guess``, ``Result``, ``Off by``
        and ``Proximity`` -- one per guess, in the order they were played.
    """
    rows = []
    for index, guess in enumerate(history, start=1):
        outcome = check_guess(guess, secret)
        rows.append(
            {
                "#": index,
                "Guess": guess,
                "Result": outcome,
                "Off by": abs(_to_int(guess, "guess") - _to_int(secret, "secret")),
                "Proximity": proximity_label(guess, secret, low, high),
            }
        )
    return rows


# ---------------------------------------------------------------------------
# High score tracking  (stretch feature: Feature Expansion via Agent Mode)
# ---------------------------------------------------------------------------


def update_high_scores(high_scores, difficulty: str, score: int, attempts: int):
    """Return a new high-score table with this result folded in.

    A result beats the stored record if it scored more points, or if it matched
    the points in fewer attempts. Ties that are no better are ignored, so the
    stored record is always the player's genuine best.

    The input mapping is never mutated -- a new dict is returned. That keeps the
    function pure and testable, and avoids the aliasing bugs that come from
    editing a dict that lives in Streamlit's session state.

    Args:
        high_scores: Existing records, mapping difficulty name to a dict with
            ``score`` and ``attempts`` keys. May be ``None`` or empty.
        difficulty: The difficulty this result was played on.
        score: The final score achieved.
        attempts: How many guesses the round took.

    Returns:
        A new mapping of difficulty name to ``{"score": int, "attempts": int}``.
    """
    updated = dict(high_scores or {})
    previous = updated.get(difficulty)

    if previous is None:
        updated[difficulty] = {"score": score, "attempts": attempts}
        return updated

    beats_on_points = score > previous["score"]
    ties_but_faster = score == previous["score"] and attempts < previous["attempts"]

    if beats_on_points or ties_but_faster:
        updated[difficulty] = {"score": score, "attempts": attempts}

    return updated


def format_high_scores(high_scores):
    """Format the high-score table for display, best difficulty first.

    Args:
        high_scores: Mapping of difficulty name to a dict with ``score`` and
            ``attempts`` keys. May be ``None`` or empty.

    Returns:
        A list of dicts with the keys ``Difficulty``, ``Best score`` and
        ``Attempts``, sorted by score descending. Empty when no rounds have
        been completed yet.
    """
    if not high_scores:
        return []

    rows = [
        {
            "Difficulty": difficulty,
            "Best score": record["score"],
            "Attempts": record["attempts"],
        }
        for difficulty, record in high_scores.items()
    ]
    rows.sort(key=lambda row: (-row["Best score"], row["Attempts"]))
    return rows
