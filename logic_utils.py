def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive (low, high) number range for the given difficulty.

    All difficulty tiers share the same 1–100 range; difficulty is expressed
    solely through the attempt limit defined in ``app.py``.  The per-tier
    ranges that existed in the original code (1–20 for Easy, 1–50 for Hard)
    caused a mismatch between the UI label and the actual valid-guess window,
    so they were removed as part of the Defect 4 fix.

    Args:
        difficulty: One of ``"Easy"``, ``"Normal"``, or ``"Hard"`` (case-
            sensitive, matching the sidebar selectbox values).

    Returns:
        A ``(low, high)`` tuple of integers representing the inclusive bounds
        of the secret number and the valid-guess range.  Always ``(1, 100)``.

    Example::

        >>> get_range_for_difficulty("Hard")
        (1, 100)
    """
    # Defect 4 Fix (range): Original code returned 1–20 for Easy and 1–50 for
    # Hard, creating a mismatch — the UI showed 1–100 but the secret was drawn
    # from a narrower range and Defect 7's validation also blocked guesses
    # above
    # that narrower bound. We spotted this by switching to Easy, guessing 50,
    # and receiving a range error even though the UI said 1–100 was valid.
    # Discussed with AI, which confirmed difficulty should be expressed through
    # attempt count alone. All tiers now return the same 1–100 range.
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """Parse and validate raw text input from the player into an integer guess.

    Performs three sequential checks before attempting numeric conversion:

    1. **Presence** — rejects ``None`` and empty strings.
    2. **Decimal guard** — rejects any string containing a ``"."`` character so
       that inputs like ``"50.9"`` are not silently truncated to ``50`` (Edge
       Case 1 fix).
    3. **Integer conversion** — passes the cleaned string to ``int()``; any
       remaining non-numeric input (letters, symbols) raises an exception that
       is caught and returned as an error.

    Range validation (1–100) is intentionally *not* performed here; it is the
    caller's responsibility so that this function remains a general-purpose
    utility independent of game-specific constants.

    Args:
        raw: The raw string value read from the Streamlit text input widget.
            May be ``None`` when the widget has never been interacted with.

    Returns:
        A three-element tuple ``(ok, guess_int, error_message)``:

        - ``ok`` (``bool``): ``True`` if parsing succeeded, ``False``
          otherwise.
        - ``guess_int`` (``int | None``): The parsed integer on success,
          ``None`` on failure.
        - ``error_message`` (``str | None``): A human-readable error string
          on failure, ``None`` on success.

    Examples::

        >>> parse_guess("42")
        (True, 42, None)

        >>> parse_guess("50.9")
        (False, None, 'Please enter a whole number.')

        >>> parse_guess("abc")
        (False, None, 'That is not a number.')

        >>> parse_guess("")
        (False, None, 'Enter a guess.')
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    # Edge Case 1 Fix Start: the original code silently truncated decimal
    # input — "50.9" was accepted and processed as 50 with no warning to the
    # player. A player who typed 50.9 intending 51 would waste an attempt
    # without knowing why the hint was wrong. We identified this during
    # edge-case analysis and discussed it with AI, which confirmed that silent
    # truncation is poor UX for
    # a whole-number guessing game. Fix: detect a "." in the raw string before
    # attempting any conversion and reject it immediately with a clear message.
    if "." in raw:
        return False, None, "Please enter a whole number."
    # Edge Case 1 Fix End

    try:
        value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """Compare the player's guess to the secret number and return a result.

    Evaluates equality first, then direction.  The directional hint strings
    were swapped in the original AI-generated code (Defect 1 – Issue 1); they
    have been corrected so that a guess above the secret returns ``"Too High"``
    with a "Go LOWER!" prompt, and a guess below returns ``"Too Low"`` with a
    "Go HIGHER!" prompt.

    Args:
        guess: The player's integer guess for the current attempt.
        secret: The secret integer that the player is trying to identify.

    Returns:
        A two-element tuple ``(outcome, message)``:

        - ``outcome`` (``str``): One of ``"Win"``, ``"Too High"``, or
          ``"Too Low"``.  Used by ``app.py`` to drive game-state transitions
          and by ``update_score`` to calculate point deltas.
        - ``message`` (``str``): A short, emoji-annotated hint string suitable
          for display directly in the Streamlit UI.

    Examples::

        >>> check_guess(50, 50)
        ('Win', '🎉 Correct!')

        >>> check_guess(80, 50)
        ('Too High', '📉 Go LOWER!')

        >>> check_guess(20, 50)
        ('Too Low', '📈 Go HIGHER!')
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # Defect 1 - Issue 1 Fix Start: The original AI-generated code had the hint
    # messages swapped — "Go HIGHER!" was shown when the guess was too high,
    # and
    # "Go LOWER!" when too low. We caught this by playing the game and noticing
    # the hints led players in the wrong direction. Collaborated with AI to
    # confirm the logic inversion, then swapped the two return strings to match
    # the conditions.
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"
    # Defect 1 - Issue 1 Fix End


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Calculate and return the new cumulative score after a single guess.

    Applies one of three scoring rules depending on the outcome:

    - **Win** — awards ``100 - 10 * (attempt_number - 1)`` points, giving a
      perfect score of 100 for a first-attempt win and decreasing by 10 for
      each additional attempt.  The minimum win bonus is clamped to 10 so that
      a win is always rewarded regardless of attempt count.
    - **Too High (even attempt)** — adds 5 points as a small bonus for
      narrowing the range from above on an even-numbered attempt.
    - **Too High (odd attempt) / Too Low** — deducts 5 points as a penalty.

    All penalty calculations are wrapped in ``max(0, ...)`` to floor the
    running total at zero and prevent negative scores (Defect 5 fix).

    Args:
        current_score: The player's accumulated score before this guess.
        outcome: The result string returned by ``check_guess``; one of
            ``"Win"``, ``"Too High"``, or ``"Too Low"``.  Any other value
            leaves ``current_score`` unchanged.
        attempt_number: The 1-based index of the current attempt (i.e., how
            many guesses the player has made including this one).

    Returns:
        The updated integer score after applying the appropriate delta.

    Examples::

        >>> update_score(0, "Win", 1)
        100

        >>> update_score(0, "Win", 3)
        80

        >>> update_score(20, "Too Low", 2)
        15

        >>> update_score(0, "Too Low", 1)
        0
    """
    # Defect 5 Fix Start: scoring formula used (attempt_number + 1) instead of
    # (attempt_number - 1), so a perfect first guess scored 80 instead of 100.
    # Wrong-guess penalties also had no floor, letting the score go negative.
    # We verified the off-by-one by tracing the formula with attempt_number=1
    # on paper; AI confirmed the correct expression and suggested max(0, ...)
    # as the standard pattern for flooring a running total at zero.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return max(0, current_score + 5)
        return max(0, current_score - 5)

    if outcome == "Too Low":
        return max(0, current_score - 5)
    # Defect 5 Fix End

    return current_score


def get_hot_cold(guess: int, secret: int) -> tuple[str, str]:
    """Return a proximity label and descriptive emoji string for a guess.

    Classifies the absolute distance between ``guess`` and ``secret`` into
    five tiers so the UI can give players an intuitive temperature-style
    signal on top of the directional hint.

    Args:
        guess: The player's integer guess for the current attempt.
        secret: The secret integer the player is trying to identify.

    Returns:
        A two-element tuple ``(label, text)``:

        - ``label`` (``str``): Machine-readable tier identifier — one of
          ``"exact"``, ``"blazing"``, ``"hot"``, ``"warm"``, ``"cold"``,
          or ``"freezing"``.  Used by ``app.py`` to choose the Streamlit
          alert colour.
        - ``text`` (``str``): Emoji-annotated string suitable for direct
          display in the UI.

    Examples::

        >>> get_hot_cold(50, 50)
        ('exact', '🎯 Exact!')

        >>> get_hot_cold(47, 50)
        ('blazing', '🔥 Blazing Hot!')

        >>> get_hot_cold(38, 50)
        ('hot', '🌶️ Hot!')

        >>> get_hot_cold(65, 50)
        ('warm', '☀️ Warm')

        >>> get_hot_cold(15, 50)
        ('cold', '❄️ Cold')

        >>> get_hot_cold(99, 50)
        ('freezing', '🧊 Freezing!')
    """
    distance = abs(guess - secret)
    if distance == 0:
        return "exact", "🎯 Exact!"
    if distance <= 5:
        return "blazing", "🔥 Blazing Hot!"
    if distance <= 10:
        return "hot", "🌶️ Hot!"
    if distance <= 20:
        return "warm", "☀️ Warm"
    if distance <= 40:
        return "cold", "❄️ Cold"
    return "freezing", "🧊 Freezing!"
