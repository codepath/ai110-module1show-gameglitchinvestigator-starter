import os
import sys

# Allow running plain `pytest` from the project root by adding the project
# root (parent of this tests/ directory) to sys.path.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_utils import check_guess, parse_guess, guess_distance, closeness, label_color, history_to_rows
from app import check_guess as app_check_guess, update_score

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

def test_too_high_hint_tells_player_to_go_lower():
    # Bug 2: a guess above the secret showed "Go HIGHER!" instead of "Go LOWER!"
    outcome, message = app_check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_hint_tells_player_to_go_higher():
    # Bug 2: a guess below the secret showed "Go LOWER!" instead of "Go HIGHER!"
    outcome, message = app_check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_too_high_always_subtracts_points():
    # Bug 3: a "Too High" guess on an even attempt added 5 points instead of subtracting them
    assert update_score(50, "Too High", attempt_number=2) == 45
    assert update_score(50, "Too High", attempt_number=3) == 45

# --- Edge case 1: negative numbers ---
# A player could type a negative number. It should parse cleanly and just be
# treated as "Too Low" (since it's below any possible secret), not crash.

def test_parse_guess_handles_negative_numbers():
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None

def test_negative_guess_is_too_low():
    result = check_guess(-5, 50)
    assert result == "Too Low"

# --- Edge case 2: decimals ---
# A player could type a decimal like "50.5". parse_guess should truncate it
# to an int (50) instead of crashing or rejecting it as "not a number".

def test_parse_guess_handles_decimal_input():
    ok, value, err = parse_guess("50.5")
    assert ok is True
    assert value == 50
    assert err is None

def test_decimal_guess_can_still_win():
    # "50.5" truncates to 50, so it should match a secret of 50
    _, value, _ = parse_guess("50.5")
    assert check_guess(value, 50) == "Win"

# --- Edge case 3: extremely large numbers ---
# A player could type a huge number (way bigger than the 1-100 range).
# Python ints don't overflow, so this should parse fine and just be "Too High".

def test_parse_guess_handles_extremely_large_numbers():
    ok, value, err = parse_guess("999999999999999999999999999999")
    assert ok is True
    assert value == 999999999999999999999999999999
    assert err is None

def test_extremely_large_guess_is_too_high():
    result = check_guess(999999999999999999999999999999, 50)
    assert result == "Too High"


# --- guess_distance tests ---

def test_guess_distance_exact():
    assert guess_distance(50, 50) == 0

def test_guess_distance_symmetric():
    assert guess_distance(60, 50) == 10
    assert guess_distance(40, 50) == 10

def test_guess_distance_str_secret():
    # glitch tolerance: coerce str secret to int
    assert guess_distance(50, "50") == 0
    assert guess_distance(60, "50") == 10

def test_guess_distance_uncoercible_returns_sentinel():
    result = guess_distance("abc", 50)
    assert result >= 1000


# --- closeness tests ---

def test_closeness_exact_hit_is_hot():
    fraction, label = closeness(0, 99)
    assert abs(fraction - 1.0) < 0.001
    assert "Hot" in label

def test_closeness_cold_at_far_distance():
    fraction, label = closeness(99, 99)
    assert fraction == 0.0
    assert "Cold" in label

def test_closeness_warm_mid_range():
    # 1 - 40/99 ≈ 0.596, which falls in the Warm band
    fraction, label = closeness(40, 99)
    assert "Warm" in label

def test_closeness_fraction_not_negative():
    # distance beyond span should clamp to 0, not go negative
    fraction, label = closeness(200, 99)
    assert fraction >= 0.0

def test_closeness_zero_span_no_crash():
    # guard against ZeroDivisionError when span is 0
    fraction, label = closeness(0, 0)
    assert isinstance(fraction, float)
    assert isinstance(label, str)


def test_label_color_maps_temperatures():
    assert label_color("🔥 Hot") == "red"
    assert label_color("🌤️ Warm") == "orange"
    assert label_color("❄️ Cold") == "blue"
    assert label_color("") == "gray"


def test_history_to_rows_handles_invalid_row():
    rows = history_to_rows([
        {"attempt": 1, "guess": "abc", "outcome": "Invalid", "fraction": None, "label": ""},
        {"attempt": 2, "guess": 50,    "outcome": "Win",     "fraction": 1.0,  "label": "🔥 Hot"},
    ])
    assert rows[0]["Temperature"] == "—" and rows[0]["Closeness %"] == "—"
    assert rows[1]["Temperature"] == "🔥 Hot" and rows[1]["Closeness %"] == "100%"
