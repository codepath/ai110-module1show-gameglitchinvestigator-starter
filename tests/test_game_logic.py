from logic_utils import (
    check_guess,
    parse_guess,
    update_score,
    get_range_for_difficulty,
    hint_for_outcome,
)


# --- check_guess: the original starter tests -------------------------------

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


# --- check_guess: edge cases (Challenge 1) ---------------------------------

def test_negative_numbers():
    # Negative guesses should still compare numerically, not crash.
    assert check_guess(-5, -1) == "Too Low"
    assert check_guess(-1, -5) == "Too High"

def test_large_numbers():
    # Very large values must not overflow or be compared as strings.
    assert check_guess(1_000_000, 999_999) == "Too High"
    assert check_guess(10, 9999999999) == "Too Low"

def test_string_comparison_regression():
    # Regression for the "secret cast to str" bug: 9 > 100 numerically is
    # False, but "9" > "100" lexicographically is True. We must get "Too Low".
    assert check_guess(9, 100) == "Too Low"


# --- parse_guess -----------------------------------------------------------

def test_parse_valid_integer():
    assert parse_guess("42") == (True, 42, None)

def test_parse_empty_and_none():
    ok, value, err = parse_guess("")
    assert ok is False and value is None and err == "Enter a guess."
    ok, value, err = parse_guess(None)
    assert ok is False and value is None

def test_parse_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False and value is None and err == "That is not a number."

def test_parse_decimal_is_truncated():
    # Decimals are accepted and truncated toward zero.
    ok, value, err = parse_guess("3.9")
    assert ok is True and value == 3 and err is None


# --- update_score ----------------------------------------------------------

def test_win_awards_more_for_fewer_attempts():
    assert update_score(0, "Win", 1) == 90
    assert update_score(0, "Win", 3) == 70

def test_win_points_floored_at_10():
    # Even after many attempts a win is worth at least 10 points.
    assert update_score(0, "Win", 50) == 10

def test_wrong_guess_is_consistent_and_never_negative():
    # Wrong guesses always cost 5 regardless of attempt parity...
    assert update_score(20, "Too High", 2) == 15
    assert update_score(20, "Too High", 3) == 15
    assert update_score(20, "Too Low", 4) == 15
    # ...and the score never goes below zero.
    assert update_score(0, "Too Low", 1) == 0


# --- get_range_for_difficulty & hints --------------------------------------

def test_difficulty_ranges():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)
    # Unknown difficulty falls back to Normal instead of crashing.
    assert get_range_for_difficulty("Impossible") == (1, 100)

def test_hints_point_in_the_right_direction():
    assert "LOWER" in hint_for_outcome("Too High")
    assert "HIGHER" in hint_for_outcome("Too Low")
