"""Tests for the game rules in logic_utils.py.

The three starter tests are kept exactly as they were written. Everything below
the "regression tests" banner was added while fixing Phase 2, and each one is
tied to a specific row in the Bug Reproduction Log in reflection.md -- the test
is written so that it FAILS against the original buggy code.

# FIX: drafted these with Claude Code ("generate pytest cases that fail against
# the old check_guess and update_score"), then rewrote the assertions myself so
# each test pins the behaviour I actually observed rather than the AI's guess.
"""

import math

import pytest

from logic_utils import (
    DIFFICULTIES,
    MAX_WIN_POINTS,
    MIN_WIN_POINTS,
    TOO_HIGH,
    TOO_LOW,
    WIN,
    build_session_table,
    check_guess,
    format_high_scores,
    get_attempt_limit,
    get_range_for_difficulty,
    hint_message,
    minimum_attempts_needed,
    parse_guess,
    proximity_label,
    proximity_trend,
    update_high_scores,
    update_score,
)

# --------------------------------------------------------------------------
# Starter tests (unchanged)
# --------------------------------------------------------------------------


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --------------------------------------------------------------------------
# Regression tests: one per bug in the Bug Reproduction Log
# --------------------------------------------------------------------------


# Bug 1 -- the hints were backwards. The old code returned
# ("Too High", "Go HIGHER!"), telling the player to move further away from the
# secret. The advice is now derived from the outcome, so it cannot disagree.
def test_too_high_hint_tells_the_player_to_go_lower():
    assert "LOWER" in hint_message(check_guess(60, 50))
    assert "HIGHER" not in hint_message(check_guess(60, 50))


def test_too_low_hint_tells_the_player_to_go_higher():
    assert "HIGHER" in hint_message(check_guess(40, 50))
    assert "LOWER" not in hint_message(check_guess(40, 50))


def test_win_hint_is_congratulations_not_a_direction():
    message = hint_message(check_guess(50, 50))
    assert "Correct" in message
    assert "HIGHER" not in message and "LOWER" not in message


# Bug 2 -- app.py stringified the secret on every even attempt, so
# `guess > secret` raised TypeError and a bare `except` fell back to comparing
# str(guess) against it. That is a LEXICOGRAPHIC compare: "9" > "50" is True,
# so 9 was reported as too high. These two cases are the exact inputs from the
# reproduction log and both failed before the fix.
@pytest.mark.parametrize(
    "guess, secret, expected",
    [
        (9, "50", TOO_LOW),  # was TOO_HIGH:  "9" sorts after "50"
        (100, "50", TOO_HIGH),  # was TOO_LOW:   "100" sorts before "50"
        (9, 50, TOO_LOW),
        (100, 50, TOO_HIGH),
    ],
)
def test_comparison_is_numeric_not_lexicographic(guess, secret, expected):
    assert check_guess(guess, secret) == expected


def test_win_is_detected_even_when_the_secret_arrives_as_a_string():
    # The old top-level `guess == secret` was False for 50 == "50", so an exact
    # hit on an even attempt only "won" by accident of the except branch.
    assert check_guess(50, "50") == WIN


def test_non_numeric_input_raises_instead_of_guessing():
    # The original swallowed TypeError and returned a confident wrong answer.
    # Failing loudly is the point: a wrong hint is worse than a crash.
    with pytest.raises(TypeError):
        check_guess("fifty", 50)
    with pytest.raises(TypeError):
        check_guess(50, None)


# Bug 3 -- scoring. "Too High" used to pay +5 on even attempts and -5 on odd
# ones, and nothing clamped the total, so four wrong guesses reached -20.
def test_wrong_guesses_score_the_same_regardless_of_attempt_parity():
    on_even = update_score(50, TOO_HIGH, attempt_number=2)
    on_odd = update_score(50, TOO_HIGH, attempt_number=3)
    assert on_even == on_odd == 45


@pytest.mark.parametrize("attempt", [1, 2, 3, 4])
def test_too_high_and_too_low_cost_the_same(attempt):
    # Parametrised over attempt number on purpose: at attempt 1 the ORIGINAL
    # buggy code also charged -5 for both, so a single-attempt assertion would
    # have passed against the bug and caught nothing. Attempt 2 is where the
    # old code paid +5 for Too High and -5 for Too Low.
    assert update_score(50, TOO_HIGH, attempt) == update_score(50, TOO_LOW, attempt)


def test_wrong_guesses_never_push_the_score_negative():
    score = 0
    for attempt, guess in enumerate([40, 30, 20, 10], start=1):
        score = update_score(score, check_guess(guess, 50), attempt)
        assert score >= 0, f"score went negative on attempt {attempt}"
    assert score == 0


def test_a_first_guess_win_is_worth_full_points():
    # The old formula was 100 - 10 * (attempt_number + 1) against an
    # already-incremented counter, so a perfect game paid 80, not 100.
    assert update_score(0, WIN, attempt_number=1) == MAX_WIN_POINTS


def test_win_points_decay_with_each_attempt_used():
    assert update_score(0, WIN, 2) == 90
    assert update_score(0, WIN, 3) == 80
    # ...and never fall below the floor, however long the game ran.
    assert update_score(0, WIN, 50) == MIN_WIN_POINTS


def test_unknown_outcome_leaves_the_score_untouched():
    assert update_score(37, "Not A Real Outcome", 1) == 37


# Bug 5 -- "Hard" used to be a narrower range (1-50) than "Normal" (1-100),
# and difficulty ranges were never checked against their attempt budgets.
def test_harder_difficulty_means_a_wider_range():
    easy_low, easy_high = get_range_for_difficulty("Easy")
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")
    assert easy_high - easy_low < normal_high - normal_low < hard_high - hard_low


def test_unknown_difficulty_falls_back_to_normal_instead_of_crashing():
    assert get_range_for_difficulty("Nightmare") == get_range_for_difficulty("Normal")
    assert get_attempt_limit("Nightmare") == get_attempt_limit("Normal")


@pytest.mark.parametrize("difficulty", sorted(DIFFICULTIES))
def test_every_difficulty_is_winnable_by_binary_search(difficulty):
    """No difficulty may advertise fewer attempts than binary search needs.

    This is the guard against the class of bug that made the game "impossible":
    a range and an attempt budget that silently disagree.
    """
    low, high = get_range_for_difficulty(difficulty)
    needed = minimum_attempts_needed(low, high)
    assert needed <= get_attempt_limit(difficulty), (
        f"{difficulty} spans {high - low + 1} numbers (needs {needed} guesses) "
        f"but only allows {get_attempt_limit(difficulty)}"
    )


@pytest.mark.parametrize("difficulty", sorted(DIFFICULTIES))
def test_binary_search_actually_wins_every_secret_in_range(difficulty):
    """Play a real perfect game against every possible secret.

    Uses only check_guess's hints to narrow the range -- if the hints were
    inverted this loop would never converge.
    """
    low, high = get_range_for_difficulty(difficulty)
    limit = get_attempt_limit(difficulty)

    for secret in range(low, high + 1):
        lo, hi, attempts = low, high, 0
        while True:
            attempts += 1
            assert (
                attempts <= limit
            ), f"{difficulty}: secret {secret} not found in {limit}"
            guess = (lo + hi) // 2
            outcome = check_guess(guess, secret)
            if outcome == WIN:
                break
            if outcome == TOO_HIGH:
                hi = guess - 1
            else:
                lo = guess + 1


# Bug 6 -- input parsing. Blank/invalid input must be rejected so the caller
# never consumes an attempt for a typo.
@pytest.mark.parametrize("raw", ["", "   ", None])
def test_blank_input_is_rejected(raw):
    ok, value, err = parse_guess(raw)
    assert ok is False and value is None and err == "Enter a guess."


@pytest.mark.parametrize("raw", ["abc", "fifty", "0x1f", "--7", "1,000", "nan"])
def test_non_numeric_input_is_rejected(raw):
    ok, value, err = parse_guess(raw)
    assert ok is False and value is None
    assert err == "That is not a number."


def test_full_width_digits_are_accepted_because_python_int_accepts_them():
    """Documents a test assumption that turned out to be wrong.

    I first asserted that "4２" (an ASCII 4 and a full-width 2) should be
    rejected. It is not: Python's int() understands any Unicode decimal digit,
    so int("4２") == 42. The parser is right and my expectation was wrong, so
    the assertion records the real behaviour instead of forcing code to match a
    guess.
    """
    assert parse_guess("4２") == (True, 42, None)


@pytest.mark.parametrize("raw", ["1e999", "-1e999"])
def test_absurdly_large_input_is_rejected_without_crashing(raw):
    # float("1e999") is inf and int(inf) raises OverflowError, which would have
    # taken the page down. Caught by this test, fixed in parse_guess.
    ok, value, err = parse_guess(raw)
    assert ok is False and value is None
    assert err == "That is not a number."


def test_surrounding_whitespace_is_tolerated():
    # Not a regression test -- this already worked, because Python's int()
    # strips surrounding whitespace on its own. Kept as a guard so a future
    # rewrite of parse_guess cannot quietly break it.
    assert parse_guess(" 42 ") == (True, 42, None)


def test_whitespace_only_input_asks_for_a_guess_rather_than_scolding():
    # The original only compared `raw == ""`, so "   " fell through to
    # int("   ") and reported "That is not a number." -- technically true but
    # the wrong instruction for someone who just hit space.
    ok, value, err = parse_guess("   ")
    assert ok is False and value is None
    assert err == "Enter a guess."


def test_fractional_guess_is_rejected_not_silently_truncated():
    # The original did int(float("3.9")) -> 3 and then scored you against a
    # number you never guessed.
    ok, value, err = parse_guess("3.9")
    assert ok is False and value is None
    assert err == "Whole numbers only -- no decimals."


def test_whole_number_written_as_a_decimal_is_accepted():
    assert parse_guess("42.0") == (True, 42, None)


def test_negative_guess_is_accepted_when_no_range_is_supplied():
    assert parse_guess("-7") == (True, -7, None)


@pytest.mark.parametrize("raw", ["0", "101", "-5", "999"])
def test_out_of_range_guesses_are_rejected_when_a_range_is_supplied(raw):
    ok, value, err = parse_guess(raw, low=1, high=100)
    assert ok is False and value is None
    assert err == "Out of range. Guess between 1 and 100."


@pytest.mark.parametrize("raw", ["1", "50", "100"])
def test_guesses_on_and_inside_the_range_boundaries_are_accepted(raw):
    ok, value, err = parse_guess(raw, low=1, high=100)
    assert ok is True and value == int(raw) and err is None


# --------------------------------------------------------------------------
# Helper sanity checks
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "low, high, expected",
    [(1, 1, 1), (1, 2, 1), (1, 8, 3), (1, 20, 5), (1, 100, 7), (1, 200, 8)],
)
def test_minimum_attempts_needed(low, high, expected):
    assert minimum_attempts_needed(low, high) == expected


def test_minimum_attempts_matches_log2_for_every_difficulty():
    for difficulty, (low, high, _attempts) in DIFFICULTIES.items():
        assert minimum_attempts_needed(low, high) == math.ceil(
            math.log2(high - low + 1)
        ), difficulty


# --------------------------------------------------------------------------
# Stretch feature: Hot/Cold proximity feedback (Enhanced Game UI)
# --------------------------------------------------------------------------


def test_exact_guess_is_a_bullseye():
    assert proximity_label(50, 50, 1, 100) == "🎯 Bullseye"


def test_proximity_gets_colder_as_the_guess_moves_away():
    # Secret 50 in a 1-100 range, so the span used for normalising is 99.
    # Distances: 0, 2 (0.020), 10 (0.101), 25 (0.253), 49 (0.495).
    labels = [proximity_label(g, 50, 1, 100) for g in (50, 52, 60, 75, 99)]
    assert labels == [
        "🎯 Bullseye",
        "🔥 Blazing hot",
        "♨️ Hot",
        "🌤️ Warm",
        "🧊 Cold",
    ]


def test_the_coldest_band_is_reachable():
    # Nothing in a 1-100 game is more than 0.495 of the span from a secret of
    # 50, so "Freezing" can only show up when the secret is near an edge.
    assert proximity_label(100, 1, 1, 100) == "❄️ Freezing"
    assert proximity_label(1, 100, 1, 100) == "❄️ Freezing"


def test_every_band_is_reachable_for_some_guess():
    """No band should be dead code -- each one must be produceable."""
    seen = {proximity_label(g, 50, 1, 100) for g in range(1, 101)}
    seen |= {proximity_label(g, 1, 1, 100) for g in range(1, 101)}
    assert seen == {
        "🎯 Bullseye",
        "🔥 Blazing hot",
        "♨️ Hot",
        "🌤️ Warm",
        "🧊 Cold",
        "❄️ Freezing",
    }


def test_proximity_is_symmetric_above_and_below_the_secret():
    assert proximity_label(40, 50, 1, 100) == proximity_label(60, 50, 1, 100)


def test_proximity_is_relative_to_the_difficulty_range():
    """The same absolute distance means different things at different sizes.

    Being 10 away is most of the board on Easy (1-20) but a near miss on
    Hard (1-200). Normalising against the range is what makes the label
    match the player's intuition.
    """
    on_easy = proximity_label(14, 5, 1, 20)  # 9 away out of 19 -> 0.474
    on_hard = proximity_label(109, 100, 1, 200)  # 9 away out of 199 -> 0.045
    assert on_easy == "🧊 Cold"
    assert on_hard == "🔥 Blazing hot"


def test_proximity_does_not_divide_by_zero_on_a_degenerate_range():
    # A range where low == high would make the span 0.
    assert proximity_label(5, 5, 5, 5) == "🎯 Bullseye"


@pytest.mark.parametrize(
    "previous, guess, expected",
    [
        (None, 40, ""),  # first guess of a round has nothing to compare to
        (20, 40, "warmer"),  # 30 away -> 10 away
        (45, 20, "colder"),  # 5 away -> 30 away
        (40, 60, "same"),  # 10 away both times, opposite sides
    ],
)
def test_proximity_trend(previous, guess, expected):
    assert proximity_trend(previous, guess, secret=50) == expected


def test_session_table_has_one_row_per_guess_in_play_order():
    rows = build_session_table([60, 40, 50], secret=50, low=1, high=100)
    assert [row["#"] for row in rows] == [1, 2, 3]
    assert [row["Guess"] for row in rows] == [60, 40, 50]
    assert [row["Result"] for row in rows] == [TOO_HIGH, TOO_LOW, WIN]
    assert [row["Off by"] for row in rows] == [10, 10, 0]
    assert rows[-1]["Proximity"] == "🎯 Bullseye"


def test_session_table_is_empty_for_a_round_with_no_guesses():
    assert build_session_table([], secret=50, low=1, high=100) == []


# --------------------------------------------------------------------------
# Stretch feature: High score tracking (Feature Expansion via Agent Mode)
# --------------------------------------------------------------------------


def test_first_result_always_sets_the_record():
    assert update_high_scores({}, "Normal", score=80, attempts=3) == {
        "Normal": {"score": 80, "attempts": 3}
    }


def test_a_higher_score_replaces_the_record():
    existing = {"Normal": {"score": 80, "attempts": 3}}
    assert update_high_scores(existing, "Normal", 90, 2)["Normal"] == {
        "score": 90,
        "attempts": 2,
    }


def test_a_lower_score_does_not_replace_the_record():
    existing = {"Normal": {"score": 90, "attempts": 2}}
    assert update_high_scores(existing, "Normal", 50, 1)["Normal"] == {
        "score": 90,
        "attempts": 2,
    }


def test_an_equal_score_in_fewer_attempts_wins_the_tie():
    existing = {"Normal": {"score": 90, "attempts": 4}}
    assert update_high_scores(existing, "Normal", 90, 2)["Normal"]["attempts"] == 2


def test_an_equal_score_in_more_attempts_does_not_win_the_tie():
    existing = {"Normal": {"score": 90, "attempts": 2}}
    assert update_high_scores(existing, "Normal", 90, 5)["Normal"]["attempts"] == 2


def test_each_difficulty_keeps_its_own_record():
    scores = update_high_scores({}, "Easy", 100, 1)
    scores = update_high_scores(scores, "Hard", 60, 5)
    assert set(scores) == {"Easy", "Hard"}
    assert scores["Easy"]["score"] == 100
    assert scores["Hard"]["score"] == 60


def test_update_high_scores_does_not_mutate_its_input():
    """Purity matters here: this dict lives in Streamlit's session state.

    Mutating it in place would make the "is this a new record?" check in
    app.py compare an object against itself and never fire.
    """
    original = {"Normal": {"score": 80, "attempts": 3}}
    snapshot = {"Normal": {"score": 80, "attempts": 3}}
    update_high_scores(original, "Normal", 100, 1)
    assert original == snapshot


def test_update_high_scores_tolerates_none():
    assert update_high_scores(None, "Easy", 70, 2) == {
        "Easy": {"score": 70, "attempts": 2}
    }


def test_high_scores_are_formatted_best_first():
    scores = {
        "Easy": {"score": 70, "attempts": 3},
        "Normal": {"score": 100, "attempts": 1},
        "Hard": {"score": 90, "attempts": 2},
    }
    assert [row["Difficulty"] for row in format_high_scores(scores)] == [
        "Normal",
        "Hard",
        "Easy",
    ]


def test_formatting_an_empty_high_score_table_gives_no_rows():
    assert format_high_scores({}) == []
    assert format_high_scores(None) == []
