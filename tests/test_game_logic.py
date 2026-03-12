import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess, update_score, get_range_for_difficulty


# --- check_guess ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

# Bug fix: hint messages were swapped
def test_too_high_says_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message

# Bug fix: secret must always be compared as int (no string type confusion)
def test_check_guess_always_uses_int_comparison():
    # Passing secret as str used to cause broken lexicographic comparison
    # e.g. "9" > "10" is True in Python — now secret is always int
    outcome, _ = check_guess(9, 10)
    assert outcome == "Too Low"  # 9 < 10, would wrongly be "Too High" with str compare


# --- update_score ---

# Bug fix: first-attempt win should score 100, not 80 (was using attempt_number + 1)
def test_win_on_first_attempt_scores_100():
    score = update_score(0, "Win", 1)
    assert score == 100

def test_win_on_second_attempt_scores_90():
    score = update_score(0, "Win", 2)
    assert score == 90

def test_win_score_minimum_is_10():
    score = update_score(0, "Win", 100)
    assert score == 10

# Bug fix: even-attempt "Too High" used to give +5 instead of -5
def test_too_high_always_deducts_5():
    assert update_score(50, "Too High", 2) == 45  # was 55 before fix
    assert update_score(50, "Too High", 3) == 45

def test_too_low_always_deducts_5():
    assert update_score(50, "Too Low", 1) == 45
    assert update_score(50, "Too Low", 2) == 45


# --- get_range_for_difficulty ---

# Bug fix: Normal and Hard ranges were swapped
def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 50)

def test_hard_range_is_largest():
    assert get_range_for_difficulty("Hard") == (1, 100)

def test_hard_range_harder_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high
