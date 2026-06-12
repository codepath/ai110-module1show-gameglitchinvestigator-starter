import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    update_score,
    parse_guess,
)

# ---------- check_guess ----------

def test_check_guess_win():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_check_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_check_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


# ---------- get_range_for_difficulty ----------

def test_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)


def test_range_hard_is_harder_than_normal():
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high


def test_range_unknown_defaults_to_normal():
    assert get_range_for_difficulty("Bogus") == (1, 100)


# ---------- parse_guess ----------

def test_parse_guess_valid_int():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_float_string_truncates_to_int():
    ok, value, err = parse_guess("12.7")
    assert ok is True
    assert value == 12
    assert err is None


def test_parse_guess_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err is not None


# ---------- update_score ----------

def test_update_score_win_adds_points():
    new_score = update_score(current_score=0, outcome="Win", attempt_number=1)
    assert new_score > 0


def test_update_score_win_has_minimum_of_ten_points():
    new_score = update_score(current_score=0, outcome="Win", attempt_number=99)
    assert new_score == 10


def test_update_score_too_high_subtracts_on_odd_attempt():
    assert update_score(100, "Too High", attempt_number=1) == 95


def test_update_score_too_high_subtracts_on_even_attempt():
    # Regression: previously gained points on even attempts. Wrong guesses
    # must always lose points, never gain.
    assert update_score(100, "Too High", attempt_number=2) == 95


def test_update_score_too_low_subtracts():
    assert update_score(100, "Too Low", attempt_number=3) == 95


def test_update_score_unknown_outcome_unchanged():
    assert update_score(100, "Mystery", attempt_number=1) == 100
