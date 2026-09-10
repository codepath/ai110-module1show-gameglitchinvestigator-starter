"""
Pytest test cases for each bug fix in the Game Glitch Investigator.
Each test targets a specific bug that was identified and fixed through user-AI collaboration.
"""

import pytest
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    get_random_attempt_limit,
)


# FIX #6: Test that all difficulties return 1-100 range
def test_range_is_1_to_100_for_all_difficulties():
    """Verify that Easy, Normal, and Hard difficulty levels use the 1-100 range."""
    assert get_range_for_difficulty("Easy") == (1, 100)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 100)


# NEW FEATURE: Test Extra Hard mode range
def test_range_for_extra_hard_is_1_to_1000():
    """Verify that Extra Hard difficulty uses the 1-1000 range."""
    assert get_range_for_difficulty("Extra Hard") == (1, 1000)


# FIX #7: Test input validation rejects numbers outside range
def test_parse_guess_rejects_number_too_high():
    """Verify that numbers >100 are rejected."""
    ok, value, error = parse_guess("150", 1, 100)
    assert ok is False
    assert value is None
    assert "between 1 and 100" in error


def test_parse_guess_rejects_number_too_low():
    """Verify that numbers <1 are rejected."""
    ok, value, error = parse_guess("0", 1, 100)
    assert ok is False
    assert value is None
    assert "between 1 and 100" in error


def test_parse_guess_accepts_valid_number():
    """Verify that numbers within range are accepted."""
    ok, value, error = parse_guess("50", 1, 100)
    assert ok is True
    assert value == 50
    assert error is None


# FIX #9: Test hint messages are correct (not reversed)
def test_check_guess_returns_correct_too_high_message():
    """Verify that guess > secret returns 'Too High' and 'Go LOWER!' message."""
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_check_guess_returns_correct_too_low_message():
    """Verify that guess < secret returns 'Too Low' and 'Go HIGHER!' message."""
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_check_guess_returns_win():
    """Verify that guess == secret returns 'Win'."""
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


# FIX #10: Test that comparisons work correctly (no string conversion bug)
def test_check_guess_with_integers_only():
    """Verify that check_guess always compares integers (no string conversion)."""
    # This would fail with the old bug where secret was converted to string
    outcome1, _ = check_guess(50, 50)
    outcome2, _ = check_guess(60, 50)
    outcome3, _ = check_guess(40, 50)

    assert outcome1 == "Win"
    assert outcome2 == "Too High"
    assert outcome3 == "Too Low"


# FIX #11: Test scoring logic is consistent
def test_update_score_win_awards_points():
    """Verify that winning awards points based on speed."""
    # Win on attempt 1 should give 90 points (100 - 10*1)
    score = update_score(0, "Win", 1)
    assert score == 90


def test_update_score_win_minimum_10_points():
    """Verify that winning always awards at least 10 points."""
    # Win on attempt 15 would be negative, but should be capped at 10
    score = update_score(0, "Win", 15)
    assert score == 10


def test_update_score_too_high_subtracts_points():
    """Verify that 'Too High' guess consistently subtracts 5 points."""
    # Test on even attempt
    score_even = update_score(100, "Too High", 2)
    assert score_even == 95  # Should subtract 5, not add

    # Test on odd attempt
    score_odd = update_score(100, "Too High", 3)
    assert score_odd == 95  # Should also subtract 5


def test_update_score_too_low_subtracts_points():
    """Verify that 'Too Low' guess subtracts 5 points."""
    score = update_score(100, "Too Low", 1)
    assert score == 95


def test_update_score_consistency():
    """Verify that both wrong guess types subtract the same amount."""
    score_from_high = update_score(100, "Too High", 1)
    score_from_low = update_score(100, "Too Low", 1)
    assert score_from_high == score_from_low == 95


# FIX #2: Test randomized attempt limits
def test_get_random_attempt_limit_easy_in_range():
    """Verify that Easy difficulty returns attempt limit between 8-12."""
    for _ in range(20):  # Test multiple times for randomness
        limit = get_random_attempt_limit("Easy")
        assert 8 <= limit <= 12


def test_get_random_attempt_limit_normal_in_range():
    """Verify that Normal difficulty returns attempt limit between 6-10."""
    for _ in range(20):
        limit = get_random_attempt_limit("Normal")
        assert 6 <= limit <= 10


def test_get_random_attempt_limit_hard_in_range():
    """Verify that Hard difficulty returns attempt limit between 4-7."""
    for _ in range(20):
        limit = get_random_attempt_limit("Hard")
        assert 4 <= limit <= 7


def test_get_random_attempt_limit_varies():
    """Verify that attempt limits are actually random (not always the same)."""
    limits = set()
    for _ in range(10):
        limits.add(get_random_attempt_limit("Normal"))
    # Should have at least 2 different values across 10 tries
    assert len(limits) >= 2


# NEW FEATURE: Test Extra Hard mode attempt limit
def test_get_random_attempt_limit_extra_hard_is_5():
    """Verify that Extra Hard difficulty always returns exactly 5 attempts."""
    for _ in range(10):
        limit = get_random_attempt_limit("Extra Hard")
        assert limit == 5


# Edge case tests
def test_parse_guess_handles_decimal_input():
    """Verify that decimal inputs are converted to integers."""
    ok, value, error = parse_guess("50.7", 1, 100)
    assert ok is True
    assert value == 50


def test_parse_guess_rejects_non_numeric():
    """Verify that non-numeric input is rejected."""
    ok, value, error = parse_guess("abc", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_rejects_empty_string():
    """Verify that empty input is rejected."""
    ok, value, error = parse_guess("", 1, 100)
    assert ok is False
    assert "Enter a guess" in error


# ============================================================================
# EDGE CASE TESTS - Testing unusual and malicious inputs
# ============================================================================

def test_parse_guess_handles_negative_number():
    """Verify that negative numbers are rejected."""
    ok, value, error = parse_guess("-5", 1, 100)
    assert ok is False
    assert "between 1 and 100" in error


def test_parse_guess_handles_large_negative_number():
    """Verify that large negative numbers are rejected."""
    ok, value, error = parse_guess("-999", 1, 100)
    assert ok is False
    assert "between 1 and 100" in error


def test_parse_guess_handles_zero():
    """Verify that zero is rejected (range starts at 1)."""
    ok, value, error = parse_guess("0", 1, 100)
    assert ok is False
    assert "between 1 and 100" in error


def test_parse_guess_handles_float_string():
    """Verify that float strings are converted to integers."""
    ok, value, error = parse_guess("42.9", 1, 100)
    assert ok is True
    assert value == 42  # Should truncate to 42
    assert error is None


def test_parse_guess_handles_negative_float():
    """Verify that negative floats are rejected."""
    ok, value, error = parse_guess("-3.14", 1, 100)
    assert ok is False
    assert "between 1 and 100" in error


def test_parse_guess_rejects_alphabetic_string():
    """Verify that alphabetic strings are rejected."""
    ok, value, error = parse_guess("hello", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_rejects_alphanumeric_string():
    """Verify that alphanumeric strings are rejected."""
    ok, value, error = parse_guess("abc123", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_rejects_special_characters():
    """Verify that special characters are rejected."""
    ok, value, error = parse_guess("@#$%", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_rejects_mathematical_expression():
    """Verify that mathematical expressions are rejected."""
    ok, value, error = parse_guess("10+5", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_rejects_multiplication_expression():
    """Verify that multiplication expressions are rejected."""
    ok, value, error = parse_guess("5*10", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_rejects_division_expression():
    """Verify that division expressions are rejected."""
    ok, value, error = parse_guess("100/2", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_handles_whitespace_around_number():
    """Verify that whitespace is handled (Python's int() strips it)."""
    ok, value, error = parse_guess("  50  ", 1, 100)
    assert ok is True
    assert value == 50


def test_parse_guess_rejects_number_with_comma():
    """Verify that numbers with commas are rejected."""
    ok, value, error = parse_guess("1,000", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_rejects_scientific_notation():
    """Verify that scientific notation is rejected."""
    ok, value, error = parse_guess("5e2", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_rejects_hex_notation():
    """Verify that hexadecimal notation is rejected."""
    ok, value, error = parse_guess("0x32", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_rejects_infinity():
    """Verify that infinity is rejected."""
    ok, value, error = parse_guess("inf", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_rejects_none_string():
    """Verify that the string 'None' is rejected."""
    ok, value, error = parse_guess("None", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_handles_none_value():
    """Verify that None value is handled gracefully."""
    ok, value, error = parse_guess(None, 1, 100)
    assert ok is False
    assert "Enter a guess" in error


def test_parse_guess_handles_boundary_minimum():
    """Verify that the minimum boundary (1) is accepted."""
    ok, value, error = parse_guess("1", 1, 100)
    assert ok is True
    assert value == 1


def test_parse_guess_handles_boundary_maximum():
    """Verify that the maximum boundary (100) is accepted."""
    ok, value, error = parse_guess("100", 1, 100)
    assert ok is True
    assert value == 100


def test_parse_guess_rejects_just_below_minimum():
    """Verify that numbers just below minimum are rejected."""
    ok, value, error = parse_guess("0", 1, 100)
    assert ok is False


def test_parse_guess_rejects_just_above_maximum():
    """Verify that numbers just above maximum are rejected."""
    ok, value, error = parse_guess("101", 1, 100)
    assert ok is False


def test_parse_guess_handles_very_large_number():
    """Verify that very large numbers are rejected."""
    ok, value, error = parse_guess("999999999", 1, 100)
    assert ok is False
    assert "between 1 and 100" in error


def test_parse_guess_handles_unicode_number():
    """Verify that unicode numbers are handled (Python int() accepts them)."""
    ok, value, error = parse_guess("５０", 1, 100)  # Full-width Japanese 50
    # Python's int() actually parses full-width unicode digits correctly!
    assert ok is True
    assert value == 50


def test_parse_guess_rejects_boolean_string():
    """Verify that boolean strings are rejected."""
    ok, value, error = parse_guess("True", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_rejects_list_notation():
    """Verify that list notation is rejected."""
    ok, value, error = parse_guess("[50]", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_rejects_dict_notation():
    """Verify that dict notation is rejected."""
    ok, value, error = parse_guess("{50}", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_handles_negative_zero():
    """Verify that -0 is handled (treated as 0, rejected)."""
    ok, value, error = parse_guess("-0", 1, 100)
    assert ok is False
    assert "between 1 and 100" in error


def test_parse_guess_rejects_multiple_decimal_points():
    """Verify that numbers with multiple decimal points are rejected."""
    ok, value, error = parse_guess("5.0.0", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_rejects_leading_zeros():
    """Verify that leading zeros are handled (should work in Python)."""
    ok, value, error = parse_guess("050", 1, 100)
    # Python's int() handles leading zeros fine
    assert ok is True
    assert value == 50


def test_parse_guess_rejects_sql_injection_attempt():
    """Verify that SQL injection attempts are rejected."""
    ok, value, error = parse_guess("50; DROP TABLE users;", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_rejects_javascript_injection():
    """Verify that JavaScript injection attempts are rejected."""
    ok, value, error = parse_guess("<script>alert('xss')</script>", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_handles_positive_sign():
    """Verify that numbers with explicit positive sign are handled."""
    ok, value, error = parse_guess("+50", 1, 100)
    # Python's int() handles + prefix
    assert ok is True
    assert value == 50


def test_parse_guess_rejects_fraction_notation():
    """Verify that fraction notation is rejected."""
    ok, value, error = parse_guess("1/2", 1, 100)
    assert ok is False
    assert "not a number" in error


def test_parse_guess_handles_exponential_that_resolves_to_valid():
    """Verify exponential notation that could be valid is still rejected."""
    # 5e1 = 50, but we reject scientific notation format
    ok, value, error = parse_guess("5e1", 1, 100)
    assert ok is False
    assert "not a number" in error
