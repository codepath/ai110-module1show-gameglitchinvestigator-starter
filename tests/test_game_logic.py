import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_utils import check_guess, get_range_for_difficulty, get_attempt_limit, update_score, parse_guess


# --- check_guess outcome (bugs 2, 7, 9) ---

def test_winning_guess():
    result = check_guess(50, 50)
    assert result[0] == "Win"

def test_guess_too_high():
    result = check_guess(60, 50)
    assert result[0] == "Too High"

def test_guess_too_low():
    result = check_guess(40, 50)
    assert result[0] == "Too Low"

# Bug 2: messages were swapped
def test_too_high_message_says_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_message_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message

# Bug 7: integer comparison always correct (no string conversion)
def test_low_guess_vs_high_secret_is_too_low():
    # 10 < 44 → player should go higher
    outcome, _ = check_guess(10, 44)
    assert outcome == "Too Low"

def test_high_guess_vs_low_secret_is_too_high():
    # 44 > 10 → player should go lower
    outcome, _ = check_guess(44, 10)
    assert outcome == "Too High"

def test_nine_vs_44_not_too_high():
    # "9" > "44" lexicographically, but 9 < 44 numerically — must use int comparison
    outcome, _ = check_guess(9, 44)
    assert outcome == "Too Low"


# --- get_range_for_difficulty (bugs 3, 5) ---

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 200

# Bug 5: Hard must be harder (larger range) than Normal
def test_hard_range_larger_than_normal():
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high

# Bug 3: Easy range must be smaller (easier) than Normal
def test_easy_range_smaller_than_normal():
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    assert easy_high < normal_high


# --- get_attempt_limit ---

def test_easy_attempt_limit():
    assert get_attempt_limit("Easy") == 10

def test_normal_attempt_limit():
    assert get_attempt_limit("Normal") == 8

def test_hard_attempt_limit():
    assert get_attempt_limit("Hard") == 5

def test_easy_more_attempts_than_hard():
    assert get_attempt_limit("Easy") > get_attempt_limit("Hard")


# --- update_score (bug 8) ---

# Bug 8: no bonus points for wrong guesses on even attempts
def test_update_score_too_high_even_attempt_subtracts():
    score = update_score(100, "Too High", 2)
    assert score == 95

def test_update_score_too_high_odd_attempt_subtracts():
    score = update_score(100, "Too High", 1)
    assert score == 95

def test_update_score_too_low_subtracts():
    score = update_score(100, "Too Low", 1)
    assert score == 95

def test_update_score_win_adds_points():
    score = update_score(0, "Win", 1)
    assert score > 0

def test_update_score_win_never_below_minimum():
    # Even on a very late attempt, win score should be at least 10
    score = update_score(0, "Win", 100)
    assert score >= 10


# --- parse_guess (bug 10) ---

def test_parse_guess_valid_integer():
    ok, val, err = parse_guess("42")
    assert ok
    assert val == 42
    assert err is None

def test_parse_guess_empty_string():
    ok, val, _ = parse_guess("")
    assert not ok
    assert val is None

def test_parse_guess_none():
    ok, _, _ = parse_guess(None)
    assert not ok

def test_parse_guess_non_numeric():
    ok, _, err = parse_guess("abc")
    assert not ok
    assert "number" in err.lower()

def test_parse_guess_float_truncates():
    ok, val, _ = parse_guess("7.9")
    assert ok
    assert val == 7
