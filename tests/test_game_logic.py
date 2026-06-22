import pytest
from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


# --- Core check_guess tests ---

def test_winning_guess():
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- Edge-case tests for parse_guess ---

def test_parse_guess_non_numeric_string():
    ok, val, err = parse_guess("abc")
    assert ok is False
    assert val is None
    assert err == "That is not a number."

def test_parse_guess_empty_string():
    ok, val, err = parse_guess("")
    assert ok is False
    assert val is None
    assert err == "Enter a guess."

def test_parse_guess_none():
    ok, val, err = parse_guess(None)
    assert ok is False
    assert val is None

def test_parse_guess_negative_number():
    ok, val, err = parse_guess("-5")
    assert ok is True
    assert val == -5
    assert err is None

def test_parse_guess_float_string():
    ok, val, err = parse_guess("42.9")
    assert ok is True
    assert val == 42
    assert err is None

def test_parse_guess_valid_integer():
    ok, val, err = parse_guess("73")
    assert ok is True
    assert val == 73
    assert err is None


# --- Edge-case tests for update_score ---

def test_score_only_increases_on_win():
    score = update_score(0, "Too High", 1)
    assert score == 0

def test_score_only_increases_on_too_low():
    score = update_score(50, "Too Low", 3)
    assert score == 50

def test_score_win_first_attempt():
    score = update_score(0, "Win", 1)
    assert score == 90

def test_score_win_clamped_at_minimum():
    score = update_score(0, "Win", 20)
    assert score == 10


# --- Difficulty range tests ---

def test_difficulty_hard_is_harder_than_normal():
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high

def test_difficulty_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20
